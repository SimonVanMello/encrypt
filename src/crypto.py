from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64


class Crypto:
	@staticmethod
	def decrypt(key: str, source: str, decode=True) -> str:
		"""
		Decrypts the given source string using AES decryption.

		Args:
			key (str): The decryption key as a string.
			source (str): The source string to be decrypted.
			decode (bool, optional): If True (default), it is assumed that the source string is base64-encoded.
									If False, the source string is expected to be raw encrypted bytes. Default is True.

		Returns:
			str: The decrypted string.

		Raises:
			ValueError: If the padding is invalid.

		Note:
			This function uses AES decryption in CBC mode with a SHA-256 derived key.
			If decode is True, the source string is assumed to be base64-encoded and is decoded before decryption.
			The function verifies and removes the padding from the decrypted result.
		"""
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


	@staticmethod
	def encrypt(key: str, source: str, encode=True):
		"""
		Encrypts the given source string using AES encryption.

		Args:
			key (str): The encryption key as a string.
			source (str): The source string to be encrypted.
			encode (bool, optional): If True (default), the result is base64-encoded and returned as a string.
									If False, the raw encrypted bytes are returned. Default is True.

		Returns:
			str or bytes: The encrypted string (base64-encoded if encode is True) or the raw encrypted bytes.

		Note:
			This function uses AES encryption in CBC mode with a SHA-256 derived key.
			The IV (Initialization Vector) is randomly generated for each encryption.
		"""
		key = key.encode()
		source = source.encode()
		key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
		IV = Random.new().read(AES.block_size)  # generate IV
		encryptor = AES.new(key, AES.MODE_CBC, IV)
		padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
		source += bytes([padding]) * padding
		data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
		return base64.b64encode(data).decode("latin-1") if encode else data