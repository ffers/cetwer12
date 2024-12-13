from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import os



def maked_hash(self):
    key = os.urandom(32)  # Ключ для AES (256 біт)
    print(key, "key")
    iv = os.urandom(16)  # IV для CBC режиму
    print(iv, "iv")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    plaintext = b"Sensitive datafsdfsdfsfsdfsdfs"
    print(plaintext, "plainttext")

    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Видаляємо padding після дешифрування
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    print(decrypted_data.decode())  # Виведе: Sensitive data