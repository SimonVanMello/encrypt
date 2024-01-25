class Settings:
	# If True: modify the file being encrypted/decrypted
	# If False: copy the file being encrypted/decrypted
	DELETE_OLD_FILE: bool = True

	# If True: ask for a single password before encrypting/decrypting
	# If False: ask a password for each file
	USE_SAME_PASSWORD_FOR_ALL_FILES: bool = False