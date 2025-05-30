# blog_blockchain/create_event.py

from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationNoOpTxn,
)
from algosdk import mnemonic
from config import ALGOD_CLIENT, CREATOR_ADDRESS, CREATOR_MNEMONIC

import sys

def call_create_event(client, private_key, app_id, event_question):
    params = client.suggested_params()

    txn = ApplicationNoOpTxn(
        sender=CREATOR_ADDRESS,
        sp=params,
        index=app_id,
        app_args=[event_question.encode()]
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)

    print(f"Sent event creation transaction with txid: {txid}")

    # Wait for confirmation (simplified)
    import time
    while True:
        try:
            pending = client.pending_transaction_info(txid)
            if pending.get("confirmed-round", 0) > 0:
                print("Event created successfully!")
                break
            else:
                print("Waiting for transaction confirmation...")
                time.sleep(2)
        except Exception:
            time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_event.py <app_id> <event_question>")
        sys.exit(1)

    app_id = int(sys.argv[1])
    event_question = sys.argv[2]

    client = ALGOD_CLIENT
    private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)

    call_create_event(client, private_key, app_id, event_question)