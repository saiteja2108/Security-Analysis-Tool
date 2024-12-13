from Crypto.Util import number
from Crypto.Random import get_random_bytes
import time

# Function to generate Diffie-Hellman parameters (1024-bit prime and generator)
def generate_dh_params(bits=1024):
    # Generate a large prime number `p`
    p = number.getPrime(bits)
    
    # Select a generator g (usually 2 is a common choice)
    g = 2
    
    return p, g

# Function to perform key generation for Diffie-Hellman
def generate_dh_keypair(p, g, bits=1024):
    # Generate a random private key (1024 bits)
    private_key = number.getRandomRange(2, p-1)  # Private key should be between 2 and p-1
    
    # Generate the public key using the formula: public_key = g^private_key mod p
    public_key = pow(g, private_key, p)
    
    return private_key, public_key

# Measure the time for generating Diffie-Hellman keys
start_time = time.time()

# Generate Diffie-Hellman parameters (1024 bits)
p, g = generate_dh_params(1024)

# Generate private and public keys for Alice and Bob
alice_private_key, alice_public_key = generate_dh_keypair(p, g)
bob_private_key, bob_public_key = generate_dh_keypair(p, g)

# Measure the key generation time
key_gen_time = time.time() - start_time

# Output the key generation time
print(f"Key Generation Time: {key_gen_time:.6f} seconds")
