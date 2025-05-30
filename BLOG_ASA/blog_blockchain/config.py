# For algod client setup via .env

# blog_blockchain/config.py

import os
from algosdk.v2client import algod
from dotenv import load_dotenv

load_dotenv()  # loads .env

ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN")

ALGOD_CLIENT = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

CREATOR_MNEMONIC = os.getenv("CREATOR_MNEMONIC")
CREATOR_ADDRESS = os.getenv("CREATOR_ADDRESS")