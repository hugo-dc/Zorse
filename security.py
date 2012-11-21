#from Crypto.Cipher import AES
import base64

sk = 'mazlibre_hugo_dc'   # App Key


def fill(string):
    while len(string) % 16 != 0:
        string += ' '
    return string

def encode(string):
    string = fill(string)
#    cipher = AES.new(sk,AES.MODE_ECB) # never use ECB in strong systems 
#    encoded = base64.b64encode(cipher.encrypt(string))
    encoded = base64.b64encode(string)
    return encoded

def decode(string):
#    cipher = AES.new(sk, AES.MODE_ECB)
#    decoded = cipher.decrypt(base64.b64decode(string))
    decoded = base64.b64decode(string)
    return decoded
