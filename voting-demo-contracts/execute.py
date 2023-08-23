import click
from web3 import Web3
from sunscreen_web3.web3 import (
    initialize_web3,
    load_or_create_account,
    deploy_libraries,
    deploy_contracts,
    export_contract_abi_to_file,
    set_account_config,
    load_contract_abi_from_file,
)
from config import Contracts, Networks
import os

__author__ = "Sunscreen Tech"

base_path = os.path.dirname(os.path.realpath(__file__))

config = None
w3 = None


@click.group()
@click.argument("network")
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
@click.argument("address")
@click.argument("private_key")
def set_account(address, private_key):
    global config
    global w3
    set_account_config(config, address, private_key)


@main.command()
def create_account():
    global config
    global w3
    account = load_or_create_account(w3)

    print("Your Account: " + account["address"])


@main.command()
def deploy():
    global config
    global w3
    account = load_or_create_account(w3)

    print("Your Account: " + account["address"])
    print(
        f"Hit ENTER once the account is funded and ready. Faucet is at {config['faucet']}"
    )
    input()

    print("Deploying libraries...")
    libraries = deploy_libraries(
        w3,
        account,
        config,
        {
            "Bytes": {"source": "contracts/libs/Bytes.sol"},
            "FHE": {"source": "contracts/libs/FHE.sol"},
        },
    )

    print("Deploying contracts...")
    contracts_parsed = {
        x["name"]: {
            "source": x["file"],
            "constructor_args": x["constructor_args"],
        }
        for x in Contracts
    }
    contracts = deploy_contracts(
        w3,
        account,
        config,
        libraries,
        contracts_parsed,
    )

    print("Exporting contract to contract.json ...")
    for cont in Contracts:
        export_contract_abi_to_file(
            contracts[cont["name"]]["address"],
            contracts[cont["name"]]["abi"],
            "contract.json",
        )
        print(
            "Contract address for "
            + cont["name"]
            + " is: "
            + contracts[cont["name"]]["address"]
        )


@main.command()
@click.argument("abi_json")
@click.argument("account_id")
def allow_account_to_vote(abi_json, account_id):
    global config
    global w3
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])
    print(
        f"Hit ENTER once the account is funded and ready. Faucet is at {config['faucet']}"
    )
    input()

    print("Loading contract from contract.json ...")
    contract = load_contract_abi_from_file(w3, config, abi_json)

    nonce = w3.eth.get_transaction_count(account["address"])
    txn = contract.functions.giveRightToVote(account_id).build_transaction(
        {
            "chainId": config["chain_id"],
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

    click.echo("Address given right to vote")


@main.command()
@click.argument("abi_json")
def get_results(abi_json):
    global w3
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])

    print("Loading contract from contract.json ...")
    contract = load_contract_abi_from_file(w3, config, abi_json)
    proposal_tallys = contract.functions.getProposalTallys().call()


if __name__ == "__main__":
    main()
