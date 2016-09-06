
if __name__ == '__main__':
    print("Import module")
    exit()

######################################################
######################################################

from Crypto.Cipher import AES

######################################################
######################################################

def encrypt(message):

    key, iv = readCrypto()

    if key and iv:

        padded = msg_pad(message)

        obj = AES.new(key, AES.MODE_CBC, iv)

        ciphertext = obj.encrypt(padded)

        return ciphertext

    return None

######################################################

def decrypt(ciphertext):

    key, iv = readCrypto()

    if key and iv:

        obj = AES.new(key, AES.MODE_CBC, iv)

        message = obj.decrypt(ciphertext)

        return msg_strip(message)

    return None

######################################################
######################################################

def getEncodedString(message):

    import base64

    encrypted = encrypt(message)

    return base64.urlsafe_b64encode(encrypted)

######################################################

def getDecodedString(encoded):

    import base64

    encrypted = base64.urlsafe_b64decode(encoded)

    return decrypt(encrypted)

######################################################
######################################################

def msg_pad(msg):
    padding = 16 - (len(msg) % 16)

    res = msg + (" " * padding)

    return res

def msg_strip(msg):
    return msg.strip(" ")

######################################################

def readCrypto():
    try:
        f = open('../config/crypto')

        key, iv = f.read().split("\n")

        f.close()

        return (key, iv)

    except IOError:
        print("crypto file not found")
        return None