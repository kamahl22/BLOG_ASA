# blog_blockchain/contracts/deploy_event_contract.py

import sys
import os
import time
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, StateSchema, OnComplete
from algosdk import mnemonic, account
from pyteal import compileTeal, Mode

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from blog_blockchain.scripts.event_contract import approval_program, clear_program
except ImportError as e:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    print(f"Import error: {e}")
    sys.exit(1)

from blog_blockchain.config import ALGOD_CLIENT, CREATOR_MNEMONIC, CREATOR_ADDRESS
def compile_teal_program(client, approval, clear):
    try:
        approval_result = client.compile(approval)
        clear_result = client.compile(clear)
        return approval_result['result'], clear_result['result']
    except Exception as e:
        print(f"Error compiling programs: {e}")
        raise

def deploy_app(client, private_key, approval_program_compiled, clear_program_compiled):
    global_schema = StateSchema(num_uints=1, num_byte_slices=3)
    local_schema = StateSchema(num_uints=2, num_byte_slices=0)
    params = client.suggested_params()

    try:
        txn = ApplicationCreateTxn(
            sender=CREATOR_ADDRESS,
            sp=params,
            on_complete=OnComplete.NoOpOC.real,
            approval_program=bytes.fromhex(approval_program_compiled),
            clear_program=bytes.fromhex(clear_program_compiled),
            global_schema=global_schema,
            local_schema=local_schema,
        )
        signed_txn = txn.sign(private_key)
        txid = client.send_transaction(signed_txn)

        while True:
            try:
                pending_txn = client.pending_transaction_info(txid)
                if pending_txn.get("confirmed-round", 0) > 0:
                    app_id = pending_txn["application-index"]
                    print(f"Deployed app with ID: {app_id}")
                    return app_id
                print("Waiting for confirmation...")
                time.sleep(2)
            except Exception as e:
                print(f"Error checking transaction: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"Error deploying app: {e}")
        raise

if __name__ == "__main__":
    client = ALGOD_CLIENT
    try:
        approval_src = compileTeal(approval_program(), mode=Mode.Application, version=6)
        clear_src = compileTeal(clear_program(), mode=Mode.Application, version=6)
    except Exception as e:
        print(f"Error compiling PyTeal programs: {e}")
        sys.exit(1)

    approval_compiled, clear_compiled = compile_teal_program(client, approval_src, clear_src)
    private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)
    app_id = deploy_app(client, private_key, approval_compiled, clear_compiled)