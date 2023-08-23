## Intro

This repository includes a sample to:
1. Deploy a contract with FHE operations
2. Interact with it as the contract owner (i.e. call owner only functions)
3. Interact with it as a contract client (i.e. call functions as a user of the contract)

## Getting Started
You can deploy and interact with contracts via our testnet or install a single-node network on your dev machine to test locally.
### Using The Test Network
The test network is deployed and available at: https://rpc.sunscreen.tech/parasol with Chain ID 574.
### Using Anvil for Local Network
1. git clone https://github.com/Sunscreen-tech/foundry
2. Go to foundry/crates
3. Execute 'cargo install --path ./anvil --bins --locked --force'
4. Execute 'anvil'
5. Your network is ready! You will have 10 accounts and 10 private keys available for use.
6. If you didn't change any defaults, your network should be available at http://127.0.0.1:8545 with Chain ID 31337.
7. You are done!

## Deploying A Contract
The deployment code exists in the 'voting-demo-contracts' folder. <br/>
The contract we will deploy exists under the 'contracts' directory. It contains the 'Ballot.sol' contract, which is the one we are deploying. 2 libraries that help provide the FHE functionality are included under the 'contracts/libs' directory. These are provided for completeness sake but you don't have to modify them.
Once you have your contract written under the 'contracts' directory, here are the steps to deploy them:
##### To the test network
1. Install all requirements by invoking 'pip install -r requirements.txt'
2. Edit config.py updated to your contract information
3. Execute 'python execute.py testnet deploy'
4. The prompt will request you to fund the account (with instructions on how)
5. You are done!
##### To Anvil (local network)
1. Install all requirements by invoking 'pip install -r requirements.txt'
2. Edit config.py updated to your contract information
3. Execute 'python execute.py local set_account --address **Account Address** --private_key **Account Private Key**'
4. Execute 'python execute.py local deploy'
5. The prompt will request you to fund the account (with instructions on how)
6. You are done!


## Interacting As Owner
##### Adding a new person to allow voting
Execute 'python execute.py <testnet/local> allow_account_to_vote --abi_json **Path to ABI JSON** --account_id **Account to allow to vote**'
##### Getting Final Vote Tally
Execute 'python execute.py <testnet/local> get_results --abi_json **Path to ABI JSON**'


## Interacting as Client
The CLI is configured under voting-demo-client-cli/python. <br/>
Execute 'pip install -r requirements.txt'
#### Configuring your account (Only for Testnets)
Execute 'python client.py testnet create_account'

#### Configuring the ABI
Copy over the contract.json from the contract folder into this folder

##### To Vote
Execute 'python client.py <testnet/local> vote --abi_json **Path to ABI JSON**'

##### To Delegate your vote
Execute 'python client.py <testnet/local> delegate --abi_json **Path to ABI JSON** --account_id **Account to delegate to**'
