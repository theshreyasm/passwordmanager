from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def generateKey(masterpassword, device_secret):

    mp = masterpassword.encode()
    salt = device_secret.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000000
    )

    key = kdf.derive(mp)

    return key


def pad(message):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message) + padder.finalize()
    return padded_data

def unpad(padded_data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
    return unpadded_data


def encrypt(key, message):

    message = message.encode()
    iv = os.urandom(16) 

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padded_message = pad(message)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    ciphertext = iv + ciphertext
    return base64.b64encode(ciphertext)


def decrypt(key, ciphertext):

    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16] 
    ciphertext = ciphertext[16:]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(decrypted_message).decode()


