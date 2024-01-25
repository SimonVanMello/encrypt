import argparse
from pathlib import Path
from file import File
from logs import Logs
from utils import Utils
from settings import Settings
from crypto import Crypto


def main():
	parser = argparse.ArgumentParser(description="Simple file encryption tool")
	parser.add_argument("files", nargs='+', help="name of the files to process")
	parser.add_argument("-d", "--decrypt", action="store_true", help="use the decryption mode")
	parser.add_argument("-v", "--verbose", action="store_true")
	args = parser.parse_args()

	files = []
	for filename in args.files:
		try:
			file = File(filename)
			if args.verbose:
				Logs.print_verbose(f"Reading file: {file.path}")
			file.read_content()
			files.append(file)
		except FileNotFoundError:
			Logs.print_error(f"File not found: {filename}")
			exit(1)
		except PermissionError:
			Logs.print_error(f"File permissions problem: {filename}")
			exit(126)

	if args.decrypt:
		decryption_password = None
		if Settings.USE_SAME_PASSWORD_FOR_ALL_FILES:
			Logs.print_warning("Using the same password for all files")
			decryption_password = Utils.get_decryption_password("all files")
		
		for file in files:
			if not file.filename.endswith(".enc"):
				Logs.print_error(f"File {file.filename} is not encrypted. Skipping")
				continue

			if not Settings.USE_SAME_PASSWORD_FOR_ALL_FILES:
				decryption_password = Utils.get_decryption_password(file.filename)
				
			try:
				decrypted_file_content = Crypto.decrypt(decryption_password, file.content)
				if args.verbose:
					Logs.print_verbose(f"Correct password")
					Logs.print_verbose(f"Creating file: {file.path[:-4]}")
				file.write_decrypted(decrypted_file_content)

				if Settings.DELETE_OLD_FILE:
					if args.verbose:
						Logs.print_verbose(f"Deleting file: {file.path}")
					file.delete()
				
				Logs.print_success(f"Decrypted file location: {file.path[:-4]}")
			except:
				Logs.print_error(f"Incorrect password")
				return

	else:
		encryption_password = None
		if Settings.USE_SAME_PASSWORD_FOR_ALL_FILES:
			Logs.print_warning("Using the same password for all files")
			encryption_password = Utils.get_encryption_password("all files")

		for file in files:
			if file.filename.endswith(".enc"):
				Logs.print_error(f"File {file.filename} is already encrypted. Skipping")
				continue

			if not Settings.USE_SAME_PASSWORD_FOR_ALL_FILES:
				encryption_password = Utils.get_encryption_password(file.filename)

			try:
				encrypted_content = Crypto.encrypt(encryption_password, file.content)
				if args.verbose:
					Logs.print_verbose(f"Creating file: {file.path}.enc")
				file.write_encrypted(encrypted_content)

				if Settings.DELETE_OLD_FILE:
					if args.verbose:
						Logs.print_verbose(f"Deleting file: {file.path}")
					file.delete()

				Logs.print_success(f"Encrypted file location: {file.path}.enc")
			except:
				Logs.print_error("An error occured")
				return


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		exit(130)
	except Exception as e:
		Logs.print_error(e)