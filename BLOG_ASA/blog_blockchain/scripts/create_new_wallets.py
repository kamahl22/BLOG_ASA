from algosdk import account, mnemonic

def create_wallet(name):
    private_key, address = account.generate_account()
    mnem = mnemonic.from_private_key(private_key)
    print(f"🔐 {name} Wallet")
    print(f"Address: {address}")
    print(f"Mnemonic: \"{mnem}\"\n")
    return address, mnem

if __name__ == "__main__":
    create_wallet("EVENT_CREATOR_WALLET")
    create_wallet("EVENT_USER_WALLET")