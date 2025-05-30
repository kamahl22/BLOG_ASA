# create_event.py

import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationCreateTxn,
    StateSchema,
    wait_for_confirmation,
)
from pyteal import compileTeal, Mode
from blog_blockchain.scripts.event_contract import approval_program, clear_program
# Load environment variables from .env or set them here:
ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"  # or your algod address
ALGOD_TOKEN = "YourPureStakeAPIKeyHere"  # or your algod token

HEADERS = {
    "X-API-Key": ALGOD_TOKEN,
}

# Creator wallet details
CREATOR_MNEMONIC = "your 25-word mnemonic here"
CREATOR_PRIVATE_KEY = mnemonic.to_private_key(CREATOR_MNEMONIC)
CREATOR_ADDRESS = account.address_from_private_key(CREATOR_PRIVATE_KEY)

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return bytes.fromhex(compile_response['result'])

def create_app(client, private_key):
    # Compile PyTeal programs to TEAL, then compile to binary for deployment
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=6)
    clear_teal = compileTeal(clear_program(), mode=Mode.Application, version=6)

    approval_program_bytes = compile_program(client, approval_teal)
    clear_program_bytes = compile_program(client, clear_teal)

    # Define schema (adjust based on your app)
    global_schema = StateSchema(num_uints=1, num_byte_slices=3)
    local_schema = StateSchema(num_uints=2, num_byte_slices=2)

    params = client.suggested_params()

    txn = ApplicationCreateTxn(
        sender=CREATOR_ADDRESS,
        sp=params,
        on_complete=0,  # NoOp
        approval_program=approval_program_bytes,
        clear_program=clear_program_bytes,
        global_schema=global_schema,
        local_schema=local_schema,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Submitted transaction with txID: {txid}")

    confirmed_txn = wait_for_confirmation(client, txid)
    app_id = confirmed_txn['application-index']
    print(f"Created new app-id: {app_id}")
    return app_id

def main():
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, headers=HEADERS)
    app_id = create_app(client, CREATOR_PRIVATE_KEY)

    print(f"Event contract deployed with App ID: {app_id}")

if __name__ == "__main__":
    main()