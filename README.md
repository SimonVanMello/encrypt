# encrypt
Just a simple python script that allows you to easily encrypt files.
## Install
```bash
git clone https://github.com/TropicoDebug/encrypt.git
cd encrypt
pip install -r requirements.txt
```
## Usage
If you are on linux i recommend you to put an alias in your .bashrc or .zshrc or equivalent for whatever shell you're using.
```
alias encrypt="python3 /path/to/encrypt.py"
```
### Commands
To encrypt a file, run:
```bash
python3 encrypt.py /path/to/file
```

Then to decrypt it:
```bash
python3 encrypt.py -d /path/to/file.enc
```
---
> I'm just a student and this code is kinda trash pls don't use it on important stuff
