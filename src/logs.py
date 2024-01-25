from bcolors import Bcolors


class Logs:
	@staticmethod
	def print_error(message: str):
		print(f"{Bcolors.FAIL}-> Error: {message}{Bcolors.ENDC}")


	@staticmethod
	def print_success(message: str) -> None:
		print(f"{Bcolors.OKGREEN}-> {message}{Bcolors.ENDC}")


	@staticmethod
	def print_verbose(message: str) -> None:
		print(f"{Bcolors.GREY}-> {message}{Bcolors.ENDC}")


	@staticmethod
	def print_warning(message: str) -> None:
		print(f"{Bcolors.WARNING}-> Warning: {message}{Bcolors.ENDC}")