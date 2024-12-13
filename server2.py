import socket
import random
from math import gcd

# Common prime modulus for simplicity
N = 10007

# Key generation and exchange functions
def generate_key_pair():
    # Generate random values a, p for Alice such that gcd(a, N) = 1
    while True:
        a = random.randint(2, N - 1)
        p = random.randint(2, N - 1)
        if gcd(a, N) == 1:
            return a, p

def calculate_value(a, p):
    # Calculate A ≡ a^p (mod N)
    return pow(a, p, N)

def calculate_session_key(value, p, a):
    # Calculate session key KA ≡ B^p + a (mod N)
    return (pow(value, p, N) + a) % N

# Start the server (Alice)
def start_server():
    # Shared agreed-upon number for both
    b = random.randint(2, N - 1)
    
    # Alice's key pair generation and calculation
    a, p = generate_key_pair()
    A = calculate_value(a, p)

    # Start the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.17.44", 8765))
    server_socket.listen(1)
    print("Alice is waiting for a connection from Bob...")

    connection, client_address = server_socket.accept()
    try:
        print("Connection established with Bob.")

        # Send Alice's value A and agreed-upon number b to Bob
        connection.sendall(f"{A},{b}".encode())
        
        # Receive Bob's value B and his chosen random number c
        data = connection.recv(1024).decode()
        B, c = map(int, data.split(","))
        
        # Calculate Alice's session key KA
        KA = calculate_session_key(B, p, a)
        print(f"Alice's session key (KA): {KA}")

    finally:
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()
