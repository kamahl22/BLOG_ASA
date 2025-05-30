# create_structure.py

import os

folders = [
    "blog_blockchain",
    "blog_blockchain/pyteal",
    "blog_blockchain/contracts",
    "blog_blockchain/deploy"
]

files = {
    "blog_blockchain/__init__.py": "",
    "blog_blockchain/pyteal/__init__.py": "",
    "blog_blockchain/config.py": "# For algod client setup via .env\n",
    ".env": "# ALGOD_TOKEN=...\n# ALGOD_ADDRESS=...\n# CREATOR_MNEMONIC=...\n",
    "requirements.txt": "pyteal\nalgosdk\npython-dotenv\n",
    "README.md": "# BLOG Prediction Market MVP\n"
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project structure created.")