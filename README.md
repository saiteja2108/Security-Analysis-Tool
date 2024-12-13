# Symmetric Key Exchange Algorithm with AVISPA Security Analysis

## Overview
This project demonstrates the implementation and performance analysis of a novel symmetric key exchange algorithm. The algorithm was developed and evaluated against established key exchange protocols, such as Diffie-Hellman and RSA, in terms of key generation time, communication time, and overall security. Additionally, the algorithm's security was validated using the AVISPA (Automated Validation of Internet Security Protocols and Applications) tool.

## Implementation
The symmetric key exchange algorithm was implemented in Python using standard libraries such as `socket`, `time`, and `random`. The algorithm employs 128-bit session keys generated through pseudo-random number generation and mathematical transformations without relying on external cryptographic libraries.

### Experimental Setup
- **Network Configuration:** A hybrid IPv4/IPv6 network topology was created using Cisco Packet Tracer.
- **Devices:**
  - **Alice (Server):** Runs the `server.py` script.
  - **Bob (Client):** Runs the `client.py` script.
  - **Mallory (Intruder):** Simulates man-in-the-middle (MITM) attacks.
- **Hardware:**
  - Intel Core i3, 4 GB RAM, running Ubuntu 22.04 LTS.
- **Router:** One Cisco Home router connects Alice and Bob for point-to-point communication.

### Key Features
1. **Hybrid Network:** Both IPv4 and IPv6 configurations supported.
2. **Efficient Key Generation:** Utilizes optimized pseudo-random number generation and mathematical transformations.
3. **Secure Communication:** Resilient against MITM attacks, verified through AVISPA analysis.

## Results
### Key Generation Time
The proposed algorithm demonstrates significantly faster key generation compared to Diffie-Hellman and RSA.

| Algorithm           | Key Size (Bytes) | Key Generation Time (ms) |
|---------------------|------------------|---------------------------|
| Proposed Algorithm  | 16               | 1.3                       |
| Diffie-Hellman      | 16               | 3.1                       |
| RSA (Asymmetric)    | 16               | 5.9                       |

### Communication Time
The proposed algorithm achieves reduced communication time due to its optimized design.

| Protocol            | Communication Time (ms) |
|---------------------|--------------------------|
| Proposed Algorithm  | 4.1                      |
| Diffie-Hellman      | 6.3                      |

### Outputs
The successful key exchange outputs from Alice and Bob are shown in Fig. 2.

## Security Analysis
The security of the proposed algorithm was analyzed using AVISPA. The following steps were performed:
1. **Modeling in HLPSL:** The key exchange algorithm was modeled in High-Level Protocol Specification Language (HLPSL).
2. **Verification in SPAN:** The model was tested in SPAN (Security Protocol Animator) on Ubuntu 10.10 Light.
3. **Results:** The AVISPA tool confirmed that the algorithm is resistant to common threats such as replay and MITM attacks.

## Usage
### Requirements
- Python 3.x
- Cisco Packet Tracer
- Ubuntu 22.04 LTS
- AVISPA Tool

### Running the Scripts
1. Set up the network topology in Cisco Packet Tracer as described.
2. Configure the machines (Alice and Bob) with hybrid IPv4/IPv6 settings.
3. Start the server:
   ```bash
   python server.py
Start the client:
bash
Copy code
python client.py
Observe the key exchange and communication results.
AVISPA Analysis
Write the HLPSL model for the protocol.
Run the AVISPA tool on the model.
Verify the results for security validation.
Future Work
Extend the algorithm to support dynamic key lengths.
Implement additional security features, such as perfect forward secrecy.
Analyze performance on more advanced hardware setups.
