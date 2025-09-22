import os
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

class AESCipher:
    def __init__(self, key: bytes):
        self.key = key
        self.bs = AES.block_size

    @staticmethod
    def from_env():
        key = os.getenv("AES_KEY", "")
        if not key:
            raise ValueError("Missing AES key in environment: AES_KEY")
        key_bytes = b64decode(key) if len(key) > 32 else key.encode()
        if len(key_bytes) != 32:
            raise ValueError("AES-256 key must be 32 bytes.")
        return AESCipher(key_bytes)

    def encrypt(self, raw: str) -> str:
        raw_bytes = raw.encode()
        iv = get_random_bytes(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enc = cipher.encrypt(pad(raw_bytes, self.bs))
        return b64encode(iv + enc).decode()

    def decrypt(self, enc: str) -> str:
        enc_bytes = b64decode(enc)
        iv = enc_bytes[:self.bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        dec = unpad(cipher.decrypt(enc_bytes[self.bs:]), self.bs)
        return dec.decode()
