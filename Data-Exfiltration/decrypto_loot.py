from cryptor import decrypt
import base64
import os
import re


def reveal_data_from_file():
    print("--- LOOT DECRYPTOR TOOL (Final Alignment) ---")

    if not os.path.exists("loot.txt"):
        print("[!] Error: 'loot.txt' not found.")
        return

    with open("loot.txt", "r") as f:
        raw_content = f.read().strip()

    # Clean only strictly necessary characters
    clean_input = re.sub(r'[^a-zA-Z0-9+/=]', '', raw_content)

    print(f"[*] Data length: {len(clean_input)} characters.")

    try:
        # 1. Manually decode base64 to check byte length
        encrypted_bytes = base64.b64decode(clean_input)
        print(f"[*] Decoded byte length: {len(encrypted_bytes)} bytes.")

        # 2. RSA 2048 MUST be 256 bytes.
        if len(encrypted_bytes) != 256:
            print(f"[!] Warning: RSA-2048 requires 256 bytes. You have {len(encrypted_bytes)}.")

        # 3. Decrypt
        decrypted_message = decrypt(clean_input)  # We pass the string to our cryptor.decrypt

        print("\n" + "=" * 35)
        print("[+] DECRYPTION SUCCESSFUL!")
        print(f"[+] Recovered: {decrypted_message.decode('utf-8')}")
        print("=" * 35)

    except Exception as e:
        print(f"\n[!] Decryption Failed: {e}")


if __name__ == '__main__':
    reveal_data_from_file()
