import asyncio
import websockets
import random
import hashlib

# Helper functions
def modular_exponentiation(base, exponent, modulus):
    return pow(base, exponent, modulus)

def generate_random_integer():
    return random.randint(1, 1_000_000)

def sign_message(message, private_key):
    # A simple hash-based "digital signature"
    return hashlib.sha256((str(message) + str(private_key)).encode()).hexdigest()

async def bob():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print(f"Connection established with Alice on port: 8765")

        # Step 1: Receive A, SA, b, and N from Alice
        message = await websocket.recv()
        A, SA, b, N = map(str, message.split(","))
        A, b, N = int(A), int(b), int(N)
        print(f"Bob received A = {A}, SA = {SA}, b = {b}, N = {N} from Alice.")

        # Step 2: Bob's calculations
        c = b  # Setting c ≡ b (mod N)
        q = generate_random_integer()  # Bob's private value q
        B = modular_exponentiation(c, q, N)  # Calculating B ≡ c^q (mod N)
        SB = sign_message(B, c)  # Bob's digital signature for B

        # Send B and SB to Alice
        await websocket.send(f"{B},{SB}")
        print(f"Bob sent B = {B} and SB = {SB} to Alice.")

        # Step 4: Verify Alice's signature for A
        if sign_message(A, b) == SA:
            print("Bob verified Alice's signature successfully.")

            # Step 5: Calculate session key KB
            KB = (modular_exponentiation(A, q, N) + c) % N
            print(f"Bob's session key KB: {KB}")

            # Step 6: Receive acknowledgment of session key establishment
            ack = await websocket.recv()
            print(ack)
            print("Session key shared and received successfully.")
        else:
            print("Bob could not verify Alice's signature.")
            await websocket.send("Signature verification failed for Alice.")

# Start Bob (Client)
asyncio.get_event_loop().run_until_complete(bob())
