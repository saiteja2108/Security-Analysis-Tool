from math import gcd
import random

# Helper function to calculate modular inverse
def mod_inverse(a, N):
    t, newt = 0, 1
    r, newr = N, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise ValueError(f"{a} has no inverse mod {N}")
    if t < 0:
        t = t + N
    return t

# Check if the values are safe
def check_safety(N, a, b, r):
    try:
        X = (mod_inverse(a, N) * b) % N
        M = (X + r) % N

        # Check conditions for safety
        ofmc_result = gcd(M, N) == 1
        cl_atse_result = M % N != 0
        satmc_result = True # No exception should be thrown if a has an inverse
        ta4sp_result = r <= N

        return ofmc_result and cl_atse_result and satmc_result and ta4sp_result
    except ValueError:
        return False

# Function to generate safe values only once
def generate_safe_values():
    N = random.getrandbits(128)
    a = random.randint(2, N - 1)
    b = random.randint(2, N - 1)
    r = random.randint(2, N - 1)

    if check_safety(N, a, b, r):
        return (N, (N + 1) % N), (a, b, r), True

    return None, None, False

# Signing function
def signing(A, private_key, N):
    a, b, r = private_key
    try:
        S = A * (a + (a ** 2) * mod_inverse(b, N) * r)
        K = (mod_inverse(a ** 2, N) * b * S) % N
    except ValueError as e:
        # print(f"Signing Error: {e}")
        return None
    return K

# AVISPA protocol simulation tools
def ofmc_simulation(public_key):
    N, M = public_key
    if gcd(M, N) != 1:
        return False, "Factoring Attack"
    return True, ""

def cl_atse_simulation(public_key):
    N, M = public_key
    if M % N == 0:
        return False, "Replay Attack / Key Reuse"
    return True, ""

def satmc_simulation(public_key, private_key):
    N, M = public_key
    a, b, r = private_key
    try:
        mod_inverse(a, N)
        return True, ""
    except ValueError:
        return False, "Key Compromise / Man-in-the-Middle Attack"

def ta4sp_simulation(public_key, private_key):
    N, M = public_key
    a, b, r = private_key
    if r > N:
        return False, "Overflow Vulnerabilities / Timing Attacks"
    return True, ""

# Full protocol analysis
def protocol_analysis():
    print("Starting protocol analysis...")
    # print("Conditions for safety:")
    # print("1. OFMC: gcd(M, N) must be 1 to prevent Factoring Attacks.")
    # print("2. CL-AtSe: M should not be a multiple of N to avoid Replay Attacks / Key Reuse.")
    # print("3. SATMC: 'a' must have a modular inverse modulo N to prevent Key Compromise / Man-in-the-Middle Attacks.")
    # print("4. TA4SP: 'r' should be less than or equal to N to avoid Overflow Vulnerabilities / Timing Attacks.")

    # Generate safe values only once
    public_key, private_key, all_safe = generate_safe_values()
    if not all_safe:
        print("Failed to generate safe values. Exiting...")
        return None

    # Verify protocol conditions
    print("Checking conditions for safety:")
    # OFMC Protocol Simulation
    ofmc_result, ofmc_message = ofmc_simulation(public_key)
    if ofmc_result:
        print("OFMC Condition: Safe")
    else:
        print(f"OFMC Condition: Unsafe. Potential Attack: {ofmc_message}")

    # CL-AtSe Protocol Simulation
    cl_atse_result, cl_atse_message = cl_atse_simulation(public_key)
    if cl_atse_result:
        print("CL-AtSe Condition: Safe")
    else:
        print(f"CL-AtSe Condition: Unsafe. Potential Attack: {cl_atse_message}")

    # SATMC Protocol Simulation
    satmc_result, satmc_message = satmc_simulation(public_key, private_key)
    if satmc_result:
        print("SATMC Condition: Safe")
    else:
        print(f"SATMC Condition: Unsafe. Potential Attack: {satmc_message}")

    # TA4SP Protocol Simulation
    ta4sp_result, ta4sp_message = ta4sp_simulation(public_key, private_key)
    if ta4sp_result:
        print("TA4SP Condition: Safe")
    else:
        print(f"TA4SP Condition: Unsafe. Potential Attack: {ta4sp_message}")

    # Overall signature verification status
    if all([ofmc_result, cl_atse_result, satmc_result, ta4sp_result]):
        print("All conditions are safe. Proceeding with message exchange...\n")
        return public_key, private_key
    else:
        print("Not all conditions are safe. Exiting...")
        return None

# Signing function for message
def sign_message(message, private_key, N):
    return signing(message, private_key, N)

# Verification function for message
def verify_signature(message, signature, public_key, private_key):
    return signing(message, private_key, public_key[0]) == signature

# message exchange protocol
# Simplified setup for key exchange (assuming message is agreed upon)
def message_exchange(alice_public_key, alice_private_key, bob_public_key, bob_private_key):
    message = random.getrandbits(128)  # A shared or agreed-upon message
    print(f"Alice's message: {message}")
    
    b, m = random.randint(2, 1000), random.randint(2, 1000)  # Alice Bob agreed upon two parameters
    p = random.randint(2, bob_public_key[0] - 1) # Bob's secret
    q = random.randint(2, bob_public_key[0] - 1) # Bob's secret
    a = b % m  # Alice's secret 
    c = b % m  # Bob's Secret 
    m = alice_public_key[0]  # Modulus (same for both)

    # Alice’s public key calculation and signature generation
    A = pow(a, p, m)  # Alice’s public parameter
    alice_signature = signing(A, alice_private_key, alice_public_key[0])

    # Bob’s public key calculation and signature generation
    B = pow(b, q, m)  # Bob’s public parameter
    bob_signature = signing(B, bob_private_key, bob_public_key[0])

    # Verification and shared secret calculation
    if verify_signature(A, alice_signature, alice_public_key, alice_private_key) and \
        verify_signature(B, bob_signature, bob_public_key, bob_private_key):

        # Alice's intermediate calculation
        alice_pow = pow(bob_public_key[1], p, m)
        K_A = alice_pow % m
        print(f"Alice's session key K_A: {K_A}")

        # Bob's intermediate calculation
        bob_pow = pow(alice_public_key[1], q, m)
        K_B = bob_pow % m
        print(f"Bob's session key K_B: {K_B}")

        # Ensure session keys match
        if K_A != K_B:
            print("Error: Session keys do not match. Exiting.")
            return
        else:
            print(f"Session keys are congruent modulo {m}.")

        # Encryption
        P = message  # The required information to send
        C = (P + (a * K_A)) % m  # Encrypt the message
        print(f"Cipher text C: {C}")

        # Decryption
        decrypted_P = (C - (c * K_B)) % m  # Decrypt the message
        print(f"Decrypted plain text P: {decrypted_P}")

        # Check if decrypted message matches original message
        if decrypted_P == P:
            print("Decryption successful! The decrypted message matches the original message.")
        else:
            print("Decryption failed. The decrypted message does not match the original message.")
    else:
        print("Signature verification failed.")


# Running the protocol analysis
keys = protocol_analysis()
if keys:
    alice_public_key, alice_private_key = keys
    bob_public_key, bob_private_key = alice_public_key, alice_private_key # Use Alice's keys for Bob for simplicity
    # Running the message exchange simulation
    message_exchange(alice_public_key, alice_private_key, bob_public_key, bob_private_key)