import os
import shutil

# Define your root project directory here (adjust if needed)
ROOT_DIR = os.path.abspath('.')

BLOG_BLOCKCHAIN_DIR = os.path.join(ROOT_DIR, 'blog_blockchain')
SCRIPTS_DIR = os.path.join(BLOG_BLOCKCHAIN_DIR, 'scripts')
CONTRACTS_DIR = os.path.join(BLOG_BLOCKCHAIN_DIR, 'contracts')
DEPLOY_DIR = os.path.join(BLOG_BLOCKCHAIN_DIR, 'deploy')
TEAL_DIR = os.path.join(BLOG_BLOCKCHAIN_DIR, 'teal')
WALLETS_DIR = os.path.join(ROOT_DIR, 'wallets')

# Files to move and their target directories
file_moves = {
    # Move top-level blockchain scripts into scripts folder
    'event_contract.py': SCRIPTS_DIR,
    'create_event.py': SCRIPTS_DIR,
    'test_transaction.py': SCRIPTS_DIR,
    'deploy_event_contract.py': DEPLOY_DIR,  # Looks like a deploy script
    'deploy_event.py': DEPLOY_DIR,
    'settle_event.py': SCRIPTS_DIR,
    'create_mvp_directory.py': SCRIPTS_DIR,  # utility script, keep in scripts

    # Contract teal files
    'event_approval.teal': CONTRACTS_DIR,
    'event_clear.teal': CONTRACTS_DIR,
}

# Wallet files to move under wallets/
wallet_files = [
    'Event_Creator_Wallet.txt',
    'Event_User_Wallet.txt',
]

def ensure_dirs():
    for d in [SCRIPTS_DIR, CONTRACTS_DIR, DEPLOY_DIR, TEAL_DIR, WALLETS_DIR]:
        if not os.path.exists(d):
            print(f"Creating directory: {d}")
            os.makedirs(d)

def move_files():
    for filename, target_dir in file_moves.items():
        src = os.path.join(ROOT_DIR, filename)
        if os.path.exists(src):
            dest = os.path.join(target_dir, filename)
            print(f"Moving {filename} to {target_dir}")
            shutil.move(src, dest)
        else:
            print(f"File {filename} not found at root, skipping.")

    for wallet_file in wallet_files:
        src = os.path.join(ROOT_DIR, wallet_file)
        if os.path.exists(src):
            dest = os.path.join(WALLETS_DIR, wallet_file)
            print(f"Moving {wallet_file} to {WALLETS_DIR}")
            shutil.move(src, dest)
        else:
            print(f"Wallet file {wallet_file} not found, skipping.")

def main():
    ensure_dirs()
    move_files()
    print("Reorganization complete. Please verify your imports in moved scripts!")

if __name__ == '__main__':
    main()