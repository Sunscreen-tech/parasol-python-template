# Parasol Python Monorepo Template
This repository includes a sample to:
1. Deploy a contract with FHE operations
2. Interact with it as a contract client (i.e. call functions as a user of the contract)

# Getting Started
You can deploy and interact with contracts via our testnet or install a single-node network on your dev machine to test locally.
First ensure the sub-modules are synced:
```sh
git submodule update --init --recursive
```

## Using The Test Network
The test network is deployed and available at: https://rpc.sunscreen.tech/parasol with Chain ID 574.

## Using `Anvil` as a local testnet
First, you'll need `cargo`; if you don't have it, the easiest way is to install via `rustup`:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

If you are on linux, also run the following:
```sh
apt update
```
```sh
apt install pkg-config
```
```sh
apt install libssl-dev
```
```sh
apt install build-essential cmake clang git
```

Then you can install our foundry fork:

```sh
cargo install --git https://github.com/Sunscreen-tech/foundry --profile local forge cast anvil --locked
```

To start your a local testnet:

```sh
anvil
```

Your network is ready! You will have 10 accounts and 10 private keys available for use. If you didn't change any defaults, your network should be available at http://127.0.0.1:8545 with Chain ID 31337.

## Install Python dependencies
```sh
pip install -r ./app/requirements.txt
```
```sh
pip install -r ./contracts/requirements.txt
```

# Deploying A Contract
The deployment code exists in the `contracts` folder. <br/>
The contract we will deploy exists under the 'src' directory. It contains the `Counter.sol` contract, which is the one we are deploying. We suggest using this as a starting point to see how the process works before modifying it.
Once you modify it, update `config.py` to match up the contract information once you edit your contracts.

## To Anvil (local network)
#### Get test account
Simply run
```sh
anvil
```
and denote one of the account and private keys that get printed.

#### Deploy

Then set up the deployment information:
```sh
cd contracts
```
```sh
python ./execute.py --network local set-account --address **Account Address** --private_key **Account Private Key**
```

Finally deploy your contract:
```sh
python ./execute.py --network local deploy
```

## To the test network
#### Create an account
First, you'll need to create an account in your wallet.
You can create the account yourself (using MetaMask, etc.) or you can execute this command to create it AND set it
```sh
cd contracts
```
```sh
python ./execute.py --network testnet create-account
```

Then, Visit the [faucet](https://faucet.sunscreen.tech/) to fund it.

Finally, denote your account's private key and address for deployment.

#### Deploy
```bash
python ./execute.py --network testnet deploy
```

If you haven't already funded your account, you'll be given a chance to do so, then hit enter.

# Interacting as A Client
```sh
cd app
```

## With The Local Network (Anvil)
#### Configuring your account
```bash
python ./client.py --network local set-account --address **Account Address** --private_key **Account Private Key**
```

#### To Increment The Counter
```bash
python ./client.py --network local increment
```

#### To Get the Current Counter
```bash
python ./client.py --network local get-number
```

#### To Set A New Number Counter
```bash
python ./client.py --network local set-number --value 10
```

## With The Test Network
#### Configuring your account
```bash
python ./client.py --network testnet create-account
```

#### To Increment The Counter
```bash
python ./client.py --network testnet increment
```

#### To Get the Current Counter
```bash
python ./client.py --network testnet get-number
```

#### To Set A New Number Counter
```bash
python ./client.py --network testnet set-number --value 10
```
