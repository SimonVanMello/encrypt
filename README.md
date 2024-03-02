# encrypt
Simple python script that allows you to easily encrypt/decrypt text files using AES encryption.
## Install
```bash
git clone https://github.com/SimonVanMello/encrypt.git
cd encrypt
pip install -r requirements.txt
```
## Usage
If you are on linux I recommend you to put an alias in your .bashrc/.zshrc or equivalent for whatever shell you're using or to put the files somewhere on your path.
```
alias encrypt="/path/to/venv/bin/python3 /path/to/main.py"
```
### Help
```
usage: main.py [-h] [-d] [-v] files [files ...]

Simple file encryption tool

positional arguments:
  files          name of the files to process

options:
  -h, --help     show this help message and exit
  -d, --decrypt  use the decryption mode
  -v, --verbose
```
### Commands
#### Encrypt
```bash
python3 main.py /path/to/files
```
#### Decrypt
```bash
python3 main.py -d /path/to/files.enc
```
## Config
You can customize a (very) few settings by editing the `settings.py` file.

---
> I'm just a student and this code is kinda trash pls don't use it on important stuff
