import sys, os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from getpass import getpass
from pathlib import Path
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loadData() -> dict:
    with open(f"{os.path.dirname(__file__)}/settings.json") as f:
        return json.load(f)

def decrypt(key: str, source: str, decode=True) -> str:
    key = key.encode()
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding].decode()  # remove the padding

def encrypt(key: str, source: str, encode=True):
    key = key.encode()
    source = source.encode()
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def readFile(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def writeFile(path: str, text: str):
    with open(path, "w") as f:
        f.write(text)

def deleteFile(path: str):
	os.remove(path)

def printHelp():
    print("--------------------------------------------------------------------------------")
    print(f"encrypt.py {bcolors.OKCYAN}-h{bcolors.ENDC} => shows this menu")
    print(f"encrypt.py {bcolors.OKCYAN}/path/to/file{bcolors.ENDC} => encrypt file (result = /path/to/file.enc)")
    print(f"encrypt.py {bcolors.OKCYAN}-d /path/to/file.enc{bcolors.ENDC} => decrypt file (result = /path/to/file)")
    print("--------------------------------------------------------------------------------")

def getPassword(confirmation: bool) -> str:
    if confirmation:
        pass1 = getpass("Encryption password: ")
        pass2 = getpass("Confirm your password: ")
        if pass1 != pass2:
            print(f"{bcolors.FAIL}-> Error: passwords mismatch{bcolors.ENDC}")
            return getPassword(confirmation)
        else: 
            return pass1
    else:
        return getpass("Decryption password: ")

def main(args: list):
    if len(args) == 0 or "-h" in args  or "--help" in args:
        printHelp()
        return
    # decrypt
    if args[0] == "-d":
        if len(args) != 2:
            printHelp()
            return
        # resolve path
        path = str(Path(args[1]).resolve())
        try:
            encryptedFile = readFile(path)
        except FileNotFoundError:
            print(f"{bcolors.FAIL}-> Error: file not found{bcolors.ENDC}")
            return
        except PermissionError:
            print(f"{bcolors.FAIL}-> Error: file permissions problem{bcolors.ENDC}")
            return
        decryptionPassword = getPassword(False)
        try:
            decryptedFile = decrypt(decryptionPassword, encryptedFile)
            writeFile(path[:-4], decryptedFile)
            print(f"{bcolors.OKGREEN}-> Correct password{bcolors.ENDC}")
            if settings["removeOriginalAfterEncryption"] == "TRUE":
                deleteFile(path)
                print(f"-> Deleted encrypted file")
            print(fr"-> Decrypted file location: {bcolors.WARNING}{path[:-4]}{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL}-> Incorrect password{bcolors.ENDC}")
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
            print(f"{bcolors.FAIL}-> Error: file not found{bcolors.ENDC}")
            return
        path += ".enc"
        password = getPassword(True)
        encryptedData = encrypt(password, dataToEncrypt)
        writeFile(path, encryptedData)
        if settings["removeOriginalAfterEncryption"] == "TRUE":
            deleteFile(path[:-4])
            print(f"-> Deleted original file")
        print(f"-> Encrypted file location: {bcolors.WARNING}{path}{bcolors.ENDC}")


try:
    print()
    settings = loadData()
    settings["removeOriginalAfterEncryption"] = settings["removeOriginalAfterEncryption"].upper()
    main(sys.argv[1:])
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"{bcolors.FAIL}-> Error:{bcolors.ENDC}\n{e}")