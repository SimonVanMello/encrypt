from getpass import getpass
from logs import Logs


class Utils:
	@staticmethod
	def get_decryption_password(filename: str) -> str:
		"""
		Prompt the user for a decryption password and return it.

		Note:
			This method uses the getpass module to securely prompt the user for a decryption password.
		"""
		return getpass(f"Decryption password for {filename}: ")


	@staticmethod
	def get_encryption_password(filename: str) -> str:
		"""
		Prompt the user for an encryption password, confirm it, and return the password.

		Note:
			This method uses the getpass module to securely prompt the user for a password.
			It confirms the entered password with a second entry and re-prompts if they don't match.
			If there is a mismatch, an error message is printed using Logs.print_error.
			The user is then prompted again for a new password.
		"""
		password = getpass(f"Encryption password for {filename}: ")
		pass_confirmation = getpass("Confirm your password: ")

		if password != pass_confirmation:
			Logs.print_error("Passwords mismatch")
			return Utils.get_encryption_password(filename)
		else: 
			return password