# blog_blockchain/pyteal/event_contract.py

from pyteal import *
import os
from pyteal import compileTeal
from pyteal import (
    Approve,
    Cond,
    Int,
    Bytes,
    Txn,
    compileTeal,
    Mode,
    Seq,
    ScratchVar,
)

def approval_program():
    # Global keys
    event_question = Bytes("event")       # Question being asked
    creator = Bytes("creator")            # Address that created this contract
    resolved = Bytes("resolved")          # Has the market resolved? (0 or 1)
    outcome = Bytes("outcome")            # Result: "YES" or "NO"

    # Local keys
    stake_yes = Bytes("stake_yes")        # ALGO staked on YES
    stake_no = Bytes("stake_no")          # ALGO staked on NO

    on_creation = Seq([
        App.globalPut(event_question, Txn.application_args[0]),
        App.globalPut(creator, Txn.sender()),
        App.globalPut(resolved, Int(0)),
        Approve()
    ])

    on_opt_in = Seq([
        App.localPut(Txn.sender(), stake_yes, Int(0)),
        App.localPut(Txn.sender(), stake_no, Int(0)),
        Approve()
    ])

    stake = Txn.application_args[0]
    amount = Btoi(Txn.application_args[1])

    on_stake_yes = Seq([
        Assert(App.globalGet(resolved) == Int(0)),
        App.localPut(Txn.sender(), stake_yes,
                     App.localGet(Txn.sender(), stake_yes) + amount),
        Approve()
    ])

    on_stake_no = Seq([
        Assert(App.globalGet(resolved) == Int(0)),
        App.localPut(Txn.sender(), stake_no,
                     App.localGet(Txn.sender(), stake_no) + amount),
        Approve()
    ])

    on_resolve = Seq([
        Assert(Txn.sender() == App.globalGet(creator)),
        App.globalPut(outcome, Txn.application_args[1]),
        App.globalPut(resolved, Int(1)),
        Approve()
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, on_opt_in],
        [Txn.application_args[0] == Bytes("YES"), on_stake_yes],
        [Txn.application_args[0] == Bytes("NO"), on_stake_no],
        [Txn.application_args[0] == Bytes("RESOLVE"), on_resolve],
    )

    return program

def clear_program():
    return Approve()


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "../contracts")
    os.makedirs(output_dir, exist_ok=True)

    approval_path = os.path.join(output_dir, "event_approval.teal")
    clear_path = os.path.join(output_dir, "event_clear.teal")

    with open(approval_path, "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)
    print(f"✅ Wrote approval program to {approval_path}")

    with open(clear_path, "w") as f:
        compiled = compileTeal(clear_program(), mode=Mode.Application, version=6)
        f.write(compiled)
    print(f"✅ Wrote clear program to {clear_path}")