from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
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

    return cipher_text, nonce



"""
Parameters: key used for encryption, encrypted text, nonce used for encryption
Decrypts text with AES CTR
Returns data in string form
"""
def aes_decrypt(key, cipher_text, nonce):
    # making sure key is proper length
    key_size = 32
    if len(key) != key_size:
        print("Improper key size: key size should be: " + str(key_size) + "\n\tkey size is: " + str(len(key)))
        exit(-1)

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    data = cipher.decrypt(cipher_text)
    data = data.decode('utf-8')

    return data


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



"""
Generates key and salt from a password
Uses scrypt; N specifies time of operation (2^14 = 100ms, 2^20 = 5s)
Returns key (bytes) and salt (bytes)
"""
def scrypt_pass(password, salt=Random.get_random_bytes(16)):
    key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
    return key, salt





"""
Raises g^a mod p
Used for Diffie Hellman where Y = g^a mod p, and K = Y^b mod p
This function uses a 4096 bit p, considered cryptographically secure for 256 bit AES key size by Rosseau
    Rousseau, F. "New Time and Space Based Key Size
                Equivalents for RSA and Diffie-Hellman", December 2000,
                http://www.sandelman.ottawa.on.ca/ipsec/2000/12/
                msg00045.html
512 bit a and b is standard - using double the bits of security of the key
(128 digits of hex)
returns Y
"""

def generate_Y(a, g=2):
    p = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C934063199FFFFFFFFFFFFFFFF'
    p = int(p, 16)
    Y = pow(g, a, p)
    return Y




