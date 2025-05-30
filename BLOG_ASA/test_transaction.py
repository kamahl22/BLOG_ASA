# test_transaction.py

import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationNoOpTxn,
    ApplicationOptInTxn,
    wait_for_confirmation,
)
from algosdk.transaction import PaymentTxn
from algosdk.logic import get_application_address

# Load environment variables or hardcode (for testing)
ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = "YourPureStakeAPIKeyHere"
HEADERS = {
    "X-API-Key": ALGOD_TOKEN,
}

# User wallet details (simulate event user)
USER_MNEMONIC = "user 25-word mnemonic here"
USER_PRIVATE_KEY = mnemonic.to_private_key(USER_MNEMONIC)
USER_ADDRESS = account.address_from_private_key(USER_PRIVATE_KEY)

# Creator wallet details (only needed to resolve event)
CREATOR_MNEMONIC = "creator 25-word mnemonic here"
CREATOR_PRIVATE_KEY = mnemonic.to_private_key(CREATOR_MNEMONIC)
CREATOR_ADDRESS = account.address_from_private_key(CREATOR_PRIVATE_KEY)

APP_ID = 12345678  # Replace with your deployed event contract App ID

def opt_in_to_app(client, app_id, private_key, sender_address):
    params = client.suggested_params()
    txn = ApplicationOptInTxn(sender=sender_address, sp=params, index=app_id)
    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    wait_for_confirmation(client, txid)
    print(f"{sender_address} opted in to app {app_id}")

def stake(client, app_id, private_key, sender_address, choice, amount):
    # choice should be "YES" or "NO"
    params = client.suggested_params()

    app_args = [choice.encode(), amount.to_bytes(8, "big")]  # amount as bytes

    txn = ApplicationNoOpTxn(
        sender=sender_address,
        sp=params,
        index=app_id,
        app_args=app_args,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    wait_for_confirmation(client, txid)
    print(f"{sender_address} staked {amount} ALGO on {choice}")

def resolve_event(client, app_id, private_key, sender_address, outcome):
    # Only creator can call resolve
    params = client.suggested_params()
    app_args = [b"RESOLVE", outcome.encode()]

    txn = ApplicationNoOpTxn(
        sender=sender_address,
        sp=params,
        index=app_id,
        app_args=app_args,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    wait_for_confirmation(client, txid)
    print(f"Event {app_id} resolved with outcome: {outcome}")

def main():
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, headers=HEADERS)

    # Opt in user to app
    opt_in_to_app(client, APP_ID, USER_PRIVATE_KEY, USER_ADDRESS)

    # Stake on YES or NO
    stake(client, APP_ID, USER_PRIVATE_KEY, USER_ADDRESS, "YES", 1000000)  # 1 ALGO in microAlgos

    # To resolve, only creator calls
    # resolve_event(client, APP_ID, CREATOR_PRIVATE_KEY, CREATOR_ADDRESS, "YES")

if __name__ == "__main__":
    main()