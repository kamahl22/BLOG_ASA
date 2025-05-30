# blog_blockchain/config.py

import os
from dotenv import load_dotenv
from algosdk import mnemonic
from algosdk.v2client import algod

# Load .env values
load_dotenv()

ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "")
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Event Creator Wallet
EVENT_CREATOR_MNEMONIC = os.getenv("EVENT_CREATOR_MNEMONIC")
EVENT_CREATOR_ADDRESS = os.getenv("EVENT_CREATOR_ADDRESS")

# Event User Wallet
EVENT_USER_MNEMONIC = os.getenv("EVENT_USER_MNEMONIC")
EVENT_USER_ADDRESS = os.getenv("EVENT_USER_ADDRESS")

# Convert mnemonics to private keys
def get_private_key(mnemonic_phrase):
    return mnemonic.to_private_key(mnemonic_phrase)

EVENT_CREATOR_PRIVATE_KEY = get_private_key(EVENT_CREATOR_MNEMONIC)
EVENT_USER_PRIVATE_KEY = get_private_key(EVENT_USER_MNEMONIC)