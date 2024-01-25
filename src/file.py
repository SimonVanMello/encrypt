import os
from logs import Logs


class File:
	def __init__(self, filename: str) -> None:
		self.filename =  filename
		self.path: str = os.path.abspath(filename)
		self.content: str = None


	def _is_encrypted(self) -> bool:
		"""
		Checks if the file associated with this instance has an ".enc" extension.

		Returns:
			bool: True if the file is encrypted (has an ".enc" extension), False otherwise.

		Note:
			This method determines whether the file path ends with the ".enc" extension,
			indicating that the file is encrypted.
		"""
		return self.path.endswith(".enc")


	def write_content(self, content: str) -> None:
		"""
		Writes the given content to the file specified by the object's path.

		Args:
			content (str): The content to be written to the file.

		Note:
			This method opens the file specified by the object's path in write mode ("w").
			It writes the provided content to the file and updates the object's internal content attribute.
			The file is automatically closed after writing.
		"""
		with open(self.path, "w") as f:
			f.write(content)
		self.content = content
	

	def read_content(self) -> None:
		"""
		Reads the content from the file specified by the object's path and updates the object's internal state.

		Note:
			This method opens the file specified by the object's path in read mode ("r").
			It reads the content from the file, updates the object's internal content attribute,
			and automatically closes the file after reading.
		"""
		with open(self.path, "r") as f:
			self.content = f.read()


	def delete(self) -> None:
		"""
		Deletes the file specified by the object's path.

		Note:
			This method removes the file located at the object's path using the os.remove function.
		"""
		os.remove(self.path)


	def write_decrypted(self, decrypted_content: str) -> None:
		"""
		Writes the decrypted content to a file, removing the ".enc" extension from the file path.

		Args:
			decrypted_content (str): The content to be written to the file.

		Note:
			This method opens a file for writing using the file path without the ".enc" extension.
			It writes the decrypted content to the file and automatically closes the file after writing.
		"""
		with open(self.path[:-4], "w") as f:
			f.write(decrypted_content)


	def write_encrypted(self, encrypted_content: str) -> None:
		"""
		Writes the encrypted content to a file, appending the ".enc" extension to the file path.

		Args:
			encrypted_content (str): The content to be written to the file.

		Note:
			This method opens a file for writing using the file path with the ".enc" extension appended.
			It writes the encrypted content to the file and automatically closes the file after writing.
		"""
		with open(f"{self.path}.enc", "w") as f:
			f.write(encrypted_content)