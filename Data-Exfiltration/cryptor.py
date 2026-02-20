from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

def generate_keys():
    key = RSA.generate(2048)
    with open("key.pri", "wb") as f: f.write(key.export_key())
    with open("key.pub", "wb") as f: f.write(key.publickey().export_key())

def encrypt(data):
    if not os.path.exists("key.pub"): generate_keys()
    recipient_key = RSA.import_key(open("key.pub").read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    # This produces exactly 256 bytes for a 2048-bit key
    return base64.b64encode(cipher_rsa.encrypt(data))

def decrypt(encrypted_data_base64):
    private_key = RSA.import_key(open("key.pri").read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(base64.b64decode(encrypted_data_base64))

if __name__ == "__main__":
    generate_keys()
    msg = b"Test connection"
    enc = encrypt(msg)
    print(f"Test Encrypted Len: {len(enc)}")
    print(f"Test Decrypted: {decrypt(enc).decode()}")
