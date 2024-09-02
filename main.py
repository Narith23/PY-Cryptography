from datetime import datetime, timedelta
import json
from cryptography.fernet import Fernet


# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    return key


# Encrypt the data
def encrypt_data(key: bytes, data: dict):
    fernet = Fernet(key)
    # Convert data to string use json
    data = json.dumps(data)
    encrypted_data = fernet.encrypt(data.encode())
    return f"{encrypted_data.decode()}.{key.decode()}"


# Decrypt the data
def decrypt_data(encrypted_data: str) -> dict:
    key = encrypted_data.split(".")[1]
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    # Json loads
    decrypted_data = json.loads(decrypted_data)

    # Convert expiration_date (which is a Unix timestamp) back to datetime object
    expiration_date = datetime.fromtimestamp(decrypted_data["expiration_date"])

    # Check if expiration_date is in the past
    current_time = datetime.now()
    if expiration_date < current_time:
        return "The data has expired."

    return decrypted_data


# Example usage
print("==============================================")
print("Step 1 - Generate encryption key")
print("==============================================")
print("")
key = generate_key()  # Keep this key safe, as you'll need it for decryption
print(f"Encryption Key: {key.decode()}")
print("")


print("==============================================")
print("Step 2 - Encrypt data")
print("==============================================")
print("")

# Expiration date is the current date plus 1 minute
expiration_date = datetime.now() + timedelta(minutes=5)

# Remove microseconds
expiration_date = expiration_date.timestamp()

data = dict(
    fields="values",
    expiration_date=expiration_date,
)
print(f"Data: {data}")
print("")


print("==============================================")
print("Step 3 - Encrypt data")
print("==============================================")
print("")
encrypted_data = encrypt_data(key, data)
print(f"Encrypted Data: {encrypted_data}")
print("")


print("==============================================")
print("Step 4 - Decrypt data")
print("==============================================")
print("")
decrypted_data = decrypt_data(encrypted_data)
print(f"Decrypted Data: {decrypted_data}")
print("")
