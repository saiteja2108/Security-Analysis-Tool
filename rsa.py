from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import time

# Measure the time taken to generate the RSA key
start_time = time.time()

# Generate the RSA 1024-bit key pair
key = RSA.generate(2048)

# Calculate the key generation time
key_gen_time = time.time() - start_time

# Export the public and private keys
private_key = key.export_key()
public_key = key.publickey().export_key()

# Print the generated keys and key generation time
print(f"RSA 1024-bit Private Key: \n{private_key.decode()}")
print(f"RSA 1024-bit Public Key: \n{public_key.decode()}")
print(f"Key Generation Time: {key_gen_time:.6f} seconds")
