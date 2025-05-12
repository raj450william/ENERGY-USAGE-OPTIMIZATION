from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
text = "user_data_example"
token = cipher.encrypt(text.encode())
print("Encrypted:", token)

# Decrypt
decrypted = cipher.decrypt(token).decode()
print("Decrypted:", decrypted)