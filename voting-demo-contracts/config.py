Contracts = [
    {
        "file": "contracts/Ballot.sol",
        "name": "Ballot",
        "constructor_args": ["What should we celebrate?", ["Christmas", "Festivus"]],
    }
]

Networks = {
    "testnet": {
        "account_file": "test_accounts.json",
        "chain_id": 0x23E,
        "rpc_endpoint": "https://rpc.sunscreen.tech/parasol",
        "faucet": "https://faucet.sunscreen.tech/",
        "solidity_version": "0.8.13",
    },
    "local": {
        "account_file": "local_accounts.json",
        "chain_id": 31337,
        "rpc_endpoint": "http://127.0.0.1:8545",
        "faucet": "No Faucet Needed for Anvil. Pick a pre-funded account from Anvil",
        "solidity_version": "0.8.13",
    },
}
