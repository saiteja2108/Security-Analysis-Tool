import socket
import random
from math import gcd

# Helper function to calculate modular inverse
def mod_inverse(a, N):
    a = a % N
    for x in range(1, N):
        if (a * x) % N == 1:
            return x
    raise ValueError(f"No modular inverse for {a} mod {N}")

# Generate public and private keys
def generate_keys(N):
    while True:
        a = random.randint(2, N - 1)
        b = random.randint(2, N - 1)
        r = random.randint(1, N)
        if gcd(a, N) == 1 and gcd(b, N) == 1:
            X = (mod_inverse(a, N) * b) % N
            M = (X + r) % N
            if gcd(M, N) == 1 and r <= N:
                return (M, N), (a, b, r)

# Sign a message
def sign_message(A, private_key, N):
    a, b, r = private_key
    S = A * (a + (a**2) * mod_inverse(b, N) * r)
    K = (mod_inverse(a**2, N) * b * S) % N
    return K

# Start the server (Alice)
def start_server():
    N = 10007  # Large prime for modulus
    public_key, private_key = generate_keys(N)
    M, N = public_key

    print(f"Alice's Public Key (M, N): ({M}, {N})")
    print(f"Alice's Private Key (a, b, r): {private_key}")

    A = 1234  # Plaintext message to sign
    K = sign_message(A, private_key, N)
    print(f"Alice's Signature: K = {K}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.17.44", 8765))
    server_socket.listen(1)
    print("Alice is waiting for a connection from Bob...")

    connection, client_address = server_socket.accept()
    try:
        print("Connection established with Bob.")
        message = f"{M},{N},{A},{K}"
        connection.sendall(message.encode())
        print(f"Sent public key (M, N) and signed message (A, K) to Bob.")
    finally:
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()
