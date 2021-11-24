from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from pyasn1.codec.der import decoder


"""
Signs data with the specified key (default is private key of root CA)
returns the signature
"""
def sign(data, key = open("./cert_auth/priv_key.pem", "r").read()):
    h = SHA256.new(data)
    rsa = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsa)
    signature = signer.sign(h)
    return signature



"""
Verifies the signature with the specified key (default is public key of root CA)
returns 1 if signature is correct, 0 if not
"""
def verify(data, signature, key = open("./cert_auth/pub_key.pem", "r").read()):
    h = SHA256.new(data)
    rsa = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsa)
    ver = 0
    if (signer.verify(h, signature)):
        ver = 1
    return ver


"""
Generates a RSA public/private key pair
Uses 2048 bit RSA with e=65537, FIPS standard
returns private, public key
"""
def generate_key_pair():
    priv = RSA.generate(2048)
    pub = priv.publickey()
    priv = priv.exportKey()
    pub = pub.exportKey()
    return priv, pub



"""
Generates a hexadecimal string from a PEM key file
if num_values is specified, the first "num_values" digits will be returned
returns hex value
"""
def pem_to_hex(key, num_values = -1):
    binary = RSA.import_key(key).export_key("DER")
    hexy = decoder.decode(binary)[0]
    number = ""
    for n in hexy:
        number += str(n)
    hexy = hex(int(number))
    if not num_values == -1:
        hexy = str(hexy)
        hexy = hexy[:num_values+2]
        hexy = hex(int(hexy, 16))
    return hexy
    


