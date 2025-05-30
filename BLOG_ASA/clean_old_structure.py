import os
import shutil

# List of files or folders to REMOVE
REMOVE_PATHS = [
    "blog_blockchain/event_factory.py",
    "blog_blockchain/__pycache__",
    "blog_blockchain/asa_utils.py",     # if it exists
    "blog_blockchain/old_scripts",      # just an example catch-all folder
]

# List of files to KEEP even if they exist elsewhere
KEEP_FILES = [
    ".env",
    "blog_blockchain/config.py",
]

def safe_delete(path):
    if os.path.isfile(path):
        if path not in KEEP_FILES:
            os.remove(path)
            print(f"🗑 Deleted file: {path}")
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f"🗑 Deleted folder: {path}")

def main():
    for path in REMOVE_PATHS:
        if os.path.exists(path):
            safe_delete(path)
        else:
            print(f"❓ Path not found, skipping: {path}")
    
    print("✅ Cleanup complete. Ready for new project structure.")

if __name__ == "__main__":
    main()