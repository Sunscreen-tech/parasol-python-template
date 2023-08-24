// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "./libs/FHE.sol";

/**
 * @title Ballot
 * @dev Implements voting process along with vote delegation
 */
contract Ballot {
    struct Voter {
        uint64 weight; // weight is accumulated by delegation
        bool voted; // if true, that person already voted
        address delegate; // person delegated to
        bytes[] votes; // index of the voted proposal
    }

    struct Proposal {
        string name;
        bytes voteCount; // number of accumulated votes
    }

    address private chairperson;

    mapping(address => Voter) private voters;

    Proposal[] private proposals;

    bytes private publicKey;
    string private ballotName;

    /**
     * @dev Create a new ballot to choose one of 'proposalNames'.
     * @param proposalNames names of proposals
     */
    constructor(string memory ballot, string[] memory proposalNames) {
        chairperson = msg.sender;
        voters[chairperson].weight = 1;
        publicKey = FHE.networkPublicKey();
        ballotName = ballot;

        for (uint i = 0; i < proposalNames.length; i++) {
            proposals.push(
                Proposal({
                    name: proposalNames[i],
                    voteCount: FHE.encryptUint256(0)
                })
            );
        }
    }

    /**
     * @dev Give 'voter' the right to vote on this ballot. May only be called by 'chairperson'.
     * @param voter address of voter
     */
    function giveRightToVote(address voter) public {
        require(
            msg.sender == chairperson,
            "Only chairperson can give right to vote."
        );
        require(!voters[voter].voted, "The voter already voted.");
        require(voters[voter].weight == 0);
        voters[voter].weight = 1;
    }

    /**
     * @dev Delegate your vote to the voter 'to'.
     * @param to address to which vote is delegated
     */
    function delegate(address to) public {
        Voter storage sender = voters[msg.sender];
        require(!sender.voted, "You already voted.");
        require(to != msg.sender, "Self-delegation is disallowed.");

        while (voters[to].delegate != address(0)) {
            to = voters[to].delegate;

            // We found a loop in the delegation, not allowed.
            require(to != msg.sender, "Found loop in delegation.");
        }
        sender.voted = true;
        sender.delegate = to;
        Voter storage delegate_ = voters[to];
        if (delegate_.voted) {
            addWeightForVotes(delegate_, sender.weight);
        } else {
            // If the delegate did not vote yet,
            // add to her weight.
            delegate_.weight += sender.weight;
        }
    }

    function addWeightForVotes(Voter memory voter, uint64 weight) private {
        for (uint i = 0; i < proposals.length; i++) {
            proposals[i].voteCount = FHE.addUint64EncEnc(
                publicKey,
                proposals[i].voteCount,
                FHE.multiplyUint64EncPlain(publicKey, voter.votes[i], weight)
            );
        }
    }

    /**
     * @dev Record your secret vote (including votes delegated to you) to the proprosals.
     * @param votes representing an array of all the propoposals.
     */
    function vote(bytes[] memory votes) public {
        Voter storage sender = voters[msg.sender];
        require(sender.weight != 0, "Has no right to vote");
        require(!sender.voted, "Already voted.");
        require(
            votes.length == proposals.length,
            "You need to give exactly as many votes as proposals"
        );
        // TODO: ZKP to ensure only 1 vote.

        sender.voted = true;
        sender.votes = votes;

        addWeightForVotes(sender, sender.weight);
    }

    /**
     * @dev Returns all the proposals to decrypt
     * @return proposals_ the proposals array
     */
    function getProposalTallys(
        bytes calldata reencPublicKey
    ) public view returns (Proposal[] memory) {
        require(
            msg.sender == chairperson,
            "Only chairperson can get the tallys."
        );

        Proposal[] memory reEncProposals = new Proposal[](proposals.length);
        for (uint i = 0; i < proposals.length; i++) {
            reEncProposals[i] = Proposal({
                name: proposals[i].name,
                voteCount: FHE.reencryptUint256(
                    reencPublicKey,
                    proposals[i].voteCount
                )
            });
        }

        return reEncProposals;
    }

    function getPublicKey() public view returns (bytes memory) {
        return publicKey;
    }

    function getBallotName() public view returns (string memory) {
        return ballotName;
    }

    function getProposals() public view returns (string[] memory) {
        string[] memory proposalNames = new string[](proposals.length);

        for (uint i = 0; i < proposals.length; i++) {
            proposalNames[i] = proposals[i].name;
        }

        return proposalNames;
    }
}
