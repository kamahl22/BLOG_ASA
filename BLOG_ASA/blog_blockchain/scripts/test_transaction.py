# blog_blockchain/test_transaction.py

from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn
from algosdk import mnemonic
from config import ALGOD_CLIENT, CREATOR_ADDRESS, CREATOR_MNEMONIC

def send_payment(client, sender_private_key, sender_address, receiver_address, amount):
    params = client.suggested_params()

    txn = PaymentTxn(
        sender=sender_address,
        sp=params,
        receiver=receiver_address,
        amt=amount
    )

    signed_txn = txn.sign(sender_private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Sent payment with txid: {txid}")

    # Wait for confirmation
    import time
    while True:
        try:
            pending = client.pending_transaction_info(txid)
            if pending.get("confirmed-round", 0) > 0:
                print("Payment transaction confirmed!")
                break
            else:
                print("Waiting for confirmation...")
                time.sleep(2)
        except Exception:
            time.sleep(2)

if __name__ == "__main__":
    client = ALGOD_CLIENT

    sender_private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)
    sender_address = CREATOR_ADDRESS

    # Replace with the receiver address you want to test payment to
    receiver_address = "RECEIVER_ALGORAND_ADDRESS_HERE"
    amount = 100000  # in microAlgos (0.1 Algo)

    send_payment(client, sender_private_key, sender_address, receiver_address, amount)