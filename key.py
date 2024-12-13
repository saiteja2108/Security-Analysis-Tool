import socket
import random
from math import gcd

# Helper functions
def mod_inverse(a, n):
    """Calculate the modular inverse of a mod n using the Extended Euclidean Algorithm."""
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError("No modular inverse exists")
    if t < 0:
        t += n
    return t

def is_valid_key(a, n):
    """Check if gcd(a, n) == 1."""
    return gcd(a, n) == 1

# Shared values
N = 2**64 + 37  # 64-bit prime
b = random.getrandbits(64)  # Shared random number (64-bit)

# Alice's private values
a = b  # a ≡ b (mod N)
p = random.getrandbits(64)  # Random private value
A = pow(a, p, N)  # A ≡ a^p (mod N)

# Generate Alice's digital signature
r = random.getrandbits(64)  # Random private value
M = (mod_inverse(a, N) * b + r) % N  # Public key
S = A * (a + a**2 * mod_inverse(b, N) * r)
K = (pow(a, -2, N) * b * S) % N  # Signature of A

# Start Server (Alice)
host = '192.168.86.44'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print("Alice (Server) listening...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Send A and its signature to Bob
        conn.sendall(f"{A},{K}".encode())
        print(f"Sent A: {A}, Signature: {K}")

        # Receive B and its signature from Bob
        data = conn.recv(4096).decode()
        if not data:
            print("Error: No data received from client!")
            conn.close()
            exit()

        try:
            B, K_b = map(int, data.split(","))
            print(f"Received B: {B}, Signature: {K_b}")
        except ValueError as e:
            print(f"Error parsing data from client: {e}")
            conn.close()
            exit()

        # Compute session key
        session_key_alice = (pow(B, p, N) + a) % N
        print(f"Session Key (Alice): {session_key_alice}")

        # Send acknowledgment to Bob
        conn.sendall("Signature verified, key exchange successful.".encode())
