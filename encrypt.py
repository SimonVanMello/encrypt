import sys
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from getpass import getpass
from pathlib import Path

def decrypt(key: str, source: str, decode=True) -> str:
    key = key.encode()
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding].decode()  # remove the padding

def encrypt(key: str, source: str, encode=True):
    key = key.encode()
    source = source.encode()
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def readFile(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def writeFile(path: str, text: str):
    with open(path, "w") as f:
        f.write(text)

def printHelp():
    print("--------------------")
    print("encrypt.py -h => shows this menu")
    print("encrypt.py /path/to/file.txt => encrypt file (result = /path/to/file.txt.enc)")
    print("encrypt.py -d /path/to/file.enc => decrypt file (result = /path/to/file.txt)")
    print("--------------------")

def getPassword(confirmation: bool) -> str:
    if confirmation:
        pass1 = getpass("Encryption password: ")
        pass2 = getpass("Confirm your password: ")
        if pass1 != pass2:
            print("-> Error: password mismatch")
            return getPassword(confirmation)
        else: 
            return pass1
    else:
        return getpass("Decryption password: ")

def main(args: list):
    if len(args) == 0 or "-h" in args:
        printHelp()
        return
    # decrypt
    if args[0] == "-d":
        if len(args) != 2:
            printHelp()
            return
        path = str(Path(args[1]).resolve())
        try:
            encryptedFile = readFile(path)
        except:
            print("-> Error: file not found")
            return
        decryptionPassword = getPassword(False)
        try:
            decryptedFile = decrypt(decryptionPassword, encryptedFile)
            writeFile(path[:-4], decryptedFile)
            print("-> Correct password")
            print(fr"-> Decrypted file location: {path[:-4]}")
        except:
            print("-> Incorrect password")
            return
    # encrypt
    else:
        if len(args) != 1:
            printHelp()
            return
        path = str(Path(args[0]).resolve())
        try:
            dataToEncrypt = readFile(path)
        except:
            print(path)
            print("-> Error: file not found")
            return
        path += ".enc"
        password = getPassword(True)
        encryptedData = encrypt(password, dataToEncrypt)
        writeFile(path, encryptedData)
        print(f"-> Encrypted file location: {path}")



main(sys.argv[1:])