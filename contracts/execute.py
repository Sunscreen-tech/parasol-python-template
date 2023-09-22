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
from config import Contracts, Networks, Remappings
import os

__author__ = "Sunscreen Tech"

base_path = os.path.dirname(os.path.realpath(__file__))

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


@main.command()
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
    if "localhost" in config["rpc_endpoint"] or "127.0.0.1" in config["rpc_endpoint"]:
        print("Can't create account for local networks. Please use other ways.")
        return

    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])


@main.command()
def deploy():
    global config
    global w3
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])
    print(
        f"Hit ENTER once the account is funded and ready. Faucet is at {config['faucet']}"
    )
    input()

    print("Deploying libraries...")
    #    libraries = deploy_libraries(
    #        w3,
    #        account,
    #        Remappings,
    #        config,
    #        {
    #            "Bytes": {"source": "contracts/libs/Bytes.sol"},
    #            "FHE": {"source": "contracts/libs/FHE.sol"},
    #        },
    #    )
    print("No libraries to deploy")
    libraries = {}

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
        Remappings,
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


if __name__ == "__main__":
    main()
