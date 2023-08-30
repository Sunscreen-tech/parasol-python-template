# Parasol Python Monorepo Template
![Solidity](https://github.com/Sunscreen-tech/hackathon-python/workflows/Solidity/badge.svg)

This repository includes a sample to:
1. Deploy a contract with FHE operations
2. Interact with it as the contract owner (i.e. call owner only functions)
3. Interact with it as a contract client (i.e. call functions as a user of the contract)

# Getting Started
You can deploy and interact with contracts via our testnet or install a single-node network on your dev machine to test locally.
## Using The Test Network
The test network is deployed and available at: https://rpc.sunscreen.tech/parasol with Chain ID 574.
## Using `Anvil` as a local testnet
First, you'll need `cargo`; if you don't have it, the easiest way is to install via `rustup`:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Then you can install our foundry fork:

```sh
cargo install --git https://github.com/Sunscreen-tech/foundry --profile local forge cast anvil
```

For more info on foundry, see the official
[docs](https://book.getfoundry.sh/).

To start your a local testnet:

```sh
anvil
```

Your network is ready! You will have 10 accounts and 10 private keys available for use. If you didn't change any defaults, your network should be available at http://127.0.0.1:8545 with Chain ID 31337.

## Installing Solidity dependencies
Forge uses submodules to manage dependencies. Initialize the dependencies:

```bash
forge install --root ./voting-demo-contracts/contracts
```

## Install Python dependencies
```bash
pip install -r ./voting-demo-contracts/requirements.txt
pip install -r ./voting-demo-client-cli/requirements.txt
```

# Testing your contract
To test your contract run:
```sh
forge test --root voting-demo-contracts/contracts
```

# Deploying A Contract
The deployment code exists in the `voting-demo-contracts` folder. <br/>
The contract we will deploy exists under the 'contracts' directory. It contains the `Ballot.sol` contract, which is the one we are deploying. We suggest using this as a starting point to see how the process works before modifying it.

## To Anvil (local network)
### Get test account
Simply run
```bash
anvil
```
and denote one of the account and private keys that get printed.

### Deploy

Then set up the deployment information:
```bash
python ./voting-demo-contracts/execute.py --network local set-account --address **Account Address** --private_key **Account Private Key**
```

Finally deploy your contract:
```bash
python execute.py --network local deploy
```
**RW: this step is broken**

## To the test network
### Create an account
First, you'll need to create an account in your wallet. Then, Visit the [faucet](https://faucet.sunscreen.tech/) to fund it.

Finally, denote your account's private key and address for deployment.

### Deploy
First, set the account:
```bash
python ./voting-demo-contracts/execute.py --network testnet set-account --address **Account Address** --private_key **Account Private Key**
```

Then, deploy:
```bash
python execute.py --network testnet deploy
```

**RW: this step is broken**

If you haven't already funded your account, you'll be given a chance to do so, then hit enter.

# Interacting As Owner
## Adding a new person to allow voting
```bash
python execute.py <testnet/local> allow-account-to-vote **Path to ABI JSON (contract.json)**  **Account to allow to vote**
```

## Getting Final Vote Tally
```bash
python execute.py <testnet/local> get-results **Path to ABI JSON (contract.json)**
```

# Interacting as Client
The CLI is configured under `voting-demo-client-cli/python`. <br/>
Execute `pip install -r requirements.txt`
## Configuring your account (Only for Testnets)
Execute `python client.py testnet create-account`
## Configuring your account (For Anvil)
Execute `python client.py local set-account **Account Address** **Account Private Key**`


# Configuring the ABI
Copy over the `contract.json` from the `contracts` folder into this folder

**RW: I don't think we need to do this anymore?**

# To Vote
```bash
python client.py <testnet/local> vote  **Path to ABI JSON (contract.json)**
```

# To Delegate your vote
```bash
python client.py <testnet/local> delegate  **Path to ABI JSON (contract.json)** **Account to delegate to**
```
