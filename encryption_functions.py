from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256

"""
Encrypts data with AES cipher
key must be 32 bytes
returns cipher text and initialization vector
"""
def aes_encrypt(data, key, init_vec = Random.get_random_bytes(AES.block_size)):
    # making sure key is proper length
    key_size = 32  # 32 bytes = 256 bits

    if len(key) != key_size:
        print("Improper key size: key size should be: " + str(key_size) + "\n\tkey size is: " + str(len(key)))
        exit(-1)

    data = data.encode('utf-8')
    data = pad(data, AES.block_size)

    # creating cipher

    cipher = AES.new(key, AES.MODE_CBC, iv = init_vec) # cipher block chaining
    cipher_text = cipher.encrypt(data)

    return cipher_text, init_vec

"""
Decrypts data with AES cipher 
key should match encoded key for accurate decryption
returns decoded message
"""
def aes_decrypt(key, cipher_text, init_vec):
   
    key_size = 32

    if len(key) != key_size:
        print("Improper key size: key size should be: " + str(key_size) + "\n\tkey size is: " + str(len(key)))
        exit(-1)

    cipher = AES.new(key, AES.MODE_CBC, init_vec)
    data = cipher.decrypt(cipher_text)

    data = unpad(data, AES.block_size)
    data = data.decode('utf-8')

    return data



from cryptography.fernet import Fernet

"""
Encrypts file with key.key
"""
def encrypt_file(filename='data.json'):
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


"""
Decrypts file with key.key
"""
def decrypt_file(filename='data.json'):
    key = open("key.key", "rb").read()
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

"""
Creates sha256 hash of string
password must be encoded
"""

def sha256_hash(password):
    h = sha256(password)
    hb = h.digest()
    return hb







