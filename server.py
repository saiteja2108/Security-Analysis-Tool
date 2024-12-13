import socket
import random

# Helper function for signature calculation based on modular exponentiation
def calculate_signature(A, b, N):
    return pow(A, b, N)  # K = A^b % N

# Common values that Alice and Bob agreed upon
b = random.getrandbits(64)  # 64-bit random number (for Alice's secret exponent)
N = random.getrandbits(128)  # 128-bit random prime modulus (simulated here)

# Alice's secret values
a = random.randint(1, N - 1)
p = random.randint(1, N - 1)
A = pow(a, p, N)  # A ≡ a^p (mod N)

# Calculate Alice's signature for A
signature_A = calculate_signature(A, b, N)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.17.44", 8765))  # Use Alice's IP address here
server_socket.listen(1)

print("Alice is waiting for a connection from Bob...")

connection, client_address = server_socket.accept()
try:
    print("Connection established with Bob.")

    # Send A, its signature, and b, N to Bob
    message_to_bob = f"{A},{signature_A},{b},{N}"
    connection.sendall(message_to_bob.encode())
    print(f"Sent A = {A}, signature_A = {signature_A}, b = {b}, and N = {N} to Bob.")

    # Receive B and signature from Bob
    data = connection.recv(1024).decode()
    B, signature_B = data.split(",")
    B = int(B)
    signature_B = int(signature_B)
    print(f"Received B = {B} and signature from Bob.")

    # Verify Bob's signature (using the same signature formula)
    if calculate_signature(B, b, N) == signature_B:
        print("Bob's signature verified.")

        # Calculate session key KA ≡ B^p + a (mod N)
        KA = (pow(B, p, N) + a) % N
        print(f"Alice's session key KA = {KA}")
    else:
        print("Signature verification failed.")
finally:
    connection.close()
    server_socket.close()
