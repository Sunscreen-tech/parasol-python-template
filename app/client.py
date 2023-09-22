import click
from web3 import Web3
from sunscreen_web3.web3 import (
    initialize_web3,
    load_or_create_account,
    load_contract_abi_from_file,
    set_account_config,
)
from sunscreen_web3.encryption import (
    SunscreenFHEContext,
    KeySet,
    EncryptedUnsigned256,
    SunscreenBuffer,
)
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
    if "localhost" in config["rpc_endpoint"] or "127.0.0.1" in config["rpc_endpoint"]:
        print("Can't create account for local networks. Please use other ways.")
        return
    account = load_or_create_account(w3, config)

    print("Your Account: " + account["address"])


@main.command()
@click.option("--abi_json", default="../contracts/contract.json")
@click.option("--value")
def set_number(abi_json, value):
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
    print("Getting public key...")
    public_key_bytes = contract.functions.getPublicKey().call()
    key_set_override = KeySet.initialize_from_buffers(
        SunscreenBuffer.create_from_bytes(bytearray(public_key_bytes))
    )

    context = SunscreenFHEContext.create_from_standard_params()

    print("Encrypting number...")
    value = int(value)
    encrypted_number = EncryptedUnsigned256.create_from_plain(
        value, context, key_set_override
    )
    encrypted_bytes = bytes(encrypted_number.get_cipher().get_bytes())

    nonce = w3.eth.get_transaction_count(account["address"])
    txn = contract.functions.setNumber(encrypted_bytes).build_transaction(
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

    print("Number Set")


@main.command()
@click.option("--abi_json", default="../contracts/contract.json")
def increment(abi_json):
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
    txn = contract.functions.increment().build_transaction(
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

    print("Incremented")


@main.command()
@click.option("--abi_json", default="../contracts/contract.json")
def get_number(abi_json):
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
    context = SunscreenFHEContext.create_from_standard_params()
    keys = context.generate_keys()
    public_key = keys.get_public_key_as_object().get_bytes()

    encrypted_bytes = contract.functions.getNumberSecretly(bytes(public_key)).call(
        {"from": account["address"]}
    )
    encrypted_value = EncryptedUnsigned256.create_from_encrypted_cipher(
        SunscreenBuffer.create_from_bytes(bytearray(encrypted_bytes)), context
    )
    print(f"Value is {encrypted_value.decrypt()}")


if __name__ == "__main__":
    main()
