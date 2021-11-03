from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256


"""
Parameters: data to be encrypted and key to encrypt with
key size is 32 bytes
encrypts with AES CTR
returns the encrypted text and nonce
"""
def aes_encrypt(data, key):
    # making sure key is proper length
    key_size = 32 # 32 bytes = 256 bits
    if len(key) != key_size:
        print("Improper key size: key size should be: " + str(key_size) + "\n\tkey size is: " + str(len(key)))
        exit(-1)

    data = data.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CTR)
    nonce = cipher.nonce
    cipher_text = cipher.encrypt(data)

    print("key")
    print(key)

    print(cipher_text)

    return cipher_text, nonce



"""
Parameters: key used for encryption, encrypted text, nonce used for encryption
Decrypts text with AES CTR
Returns data in string form
"""
def aes_decrypt(key, cipher_text, nonce):

    key_size = 32
    if len(key) != key_size:
        print("Improper key size: key size should be: " + str(key_size) + "\n\tkey size is: " + str(len(key)))
        exit(-1)

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    data = cipher.decrypt(cipher_text)

    print(data)

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
returns bytes object
"""

def sha256_hash(password, hexdigest = 0):
    h = sha256(password)
    if hexdigest == 0:
        hb = h.digest()
    else:
        hb = h.hexdigest()
    return hb



"""
Returns the hexadecimal hash of a file
input the file to be hashed
"""

def hash_file(file):

    # buffer size for large files
    BUF_SIZE = 65536

    collective_data = sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)

            # True if eof = 1
            if not data:
                break

            collective_data.update(data)

    return collective_data.hexdigest()







