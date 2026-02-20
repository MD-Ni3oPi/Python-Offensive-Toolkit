import requests
from cryptor import encrypt


def exfiltrate_to_burp(data):
    url = "https://127.0.0.1:4433/secure_sync"

    # NEW PORT: 8085
    proxies = {
        "http": "http://127.0.0.1:8085",
        "https": "http://127.0.0.1:8085",
    }

    print(f"[*] Targeting Burp on Port 8085...")
    print("[*] Encrypting data...")
    payload = encrypt(data).decode()

    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.post(
            url,
            data=payload,
            proxies=proxies,
            verify=False,
            timeout=10
        )
        if response.status_code == 200:
            print("[+] Success! Traffic caught by Burp.")

    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == '__main__':
    exfiltrate_to_burp(b"BURP_PORT_8085_TEST")
