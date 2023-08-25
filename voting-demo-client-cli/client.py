import click
from web3 import Web3
from sunscreen_web3.web3 import (
    initialize_web3,
    load_or_create_account,
    load_contract_abi_from_file,
    set_account_config,
)
from sunscreen_web3.encryption import SunscreenFHEContext, KeySet, EncryptedUnsigned256
from config import Networks

__author__ = "Sunscreen Tech"

config = None
w3 = None


@click.group()
@click.option("--network")
def main(network):
    """
    Simple CLI for Ballots
    """
    global config
    global w3
    config = Networks[network.lower()]
    w3 = initialize_web3(config)
    pass


@main.command
@click.option("--address")
@click.option("--private_key")
def set_account(address, private_key):
    global config
    global w3
    set_account_config(config, address, private_key)


@main.command()
def create_account():
    global config
    global w3
    if 'localhost' in config['rpc_endpoint'] or '127.0.0.1' in config['rpc_endpoint']:
        print("Can't create account for local networks. Please use other ways.")
        return
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])


@main.command()
@click.option("--abi_json", default="../voting-demo-contracts/contract.json")
def vote(abi_json):
    global config
    global w3
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])
    print(
        f"Hit ENTER once the account is funded and ready. Faucet is at {config['faucet']}"
    )
    input()

    print("Loading contract from contract.json ...")
    contract = load_contract_abi_from_file(w3, abi_json)
    ballot_name = contract.functions.getBallotName().call()
    proposal_names = contract.functions.getProposals().call()

    print("Ballot Name: " + ballot_name)
    for idx, x in enumerate(proposal_names):
        print("Proposal Option: " + str(idx) + " " + x)

    proposal_option = None
    while True:
        try:
            proposal_option = int(
                input("Enter the proposal number you would like to vote for: ")
            )
            if proposal_option < 0 or proposal_option >= len(proposal_names):
                print("Invalid proposal option")
            break
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            print("Error parsing your option")

    votes = [0] * len(proposal_names)
    votes[proposal_option] = 1

    print("Getting public key...")
    public_key_bytes = contract.functions.getPublicKey().call()
    key_set = KeySet.initialize_from_bytes_with_public_key(bytearray(public_key_bytes))
    context = SunscreenFHEContext.create_from_params_as_specified(4096, 4096)

    print("Encrypting responses...")
    encrypted_votes = [
        EncryptedUnsigned256.create_from_plain(x, context, key_set) for x in votes
    ]
    print("Sending response to contract")
    encrypted_votes = [bytes(x.get_bytes()) for x in encrypted_votes]
    print(len(encrypted_votes[0]))

    nonce = w3.eth.get_transaction_count(account["address"])
    txn = contract.functions.vote(encrypted_votes).build_transaction(
        {
            "chainId": config['chain_id'],
            "gasPrice": w3.eth.gas_price,
            "from": account["address"],
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(
        txn, private_key=account["private_key"]
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Executing transaction...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Votes recorded")


@main.command()
@click.option("--account_id")
@click.option("--abi_json", default="../voting-demo-contracts/contract.json")
def delegate(account_id, abi_json):
    global config
    global w3
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])
    print(
        f"Hit ENTER once the account is funded and ready. Faucet is at {config['faucet']}"
    )
    input()

    print("Loading contract from contract.json ...")
    contract = load_contract_abi_from_file(w3, abi_json)

    nonce = w3.eth.get_transaction_count(account["address"])
    txn = contract.functions.delegate(account_id).build_transaction(
        {
            "chainId": config['chain_id'],
            "gasPrice": w3.eth.gas_price,
            "from": account["address"],
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(
        txn, private_key=account["private_key"]
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Executing transaction...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    click.echo("Your vote is delegated")


if __name__ == "__main__":
    main()
