# DSS (Digital Signature Standard)

## Introduction
The Digital Signature Standard (DSS) is a standard for digital signatures. It was proposed by the National Institute of Standards and Technology (NIST) in August 1991 for use in their Digital Signature Algorithm (DSA), specified in FIPS 186 and adopted as FIPS 186-1 in 1996. The standard was withdrawn in 2013.

The DSS is based on the concept of a digital signature, which is a mathematical scheme for verifying the authenticity of digital messages or documents. A valid digital signature gives a recipient reason to believe that the message was created by a known sender, and that it was not altered in transit.

## Working of the DSS

The Digital Signature Standard (DSS) works in the following way:

1. **Key Generation**: The DSS uses a pair of keys, a private key and a public key. The private key is used to sign messages, while the public key is used to verify the signature. The private key is generated randomly and kept secret, while the public key is derived from the private key and made public.

2. **Signing**: To sign a message, the sender uses their private key to generate a digital signature. The signature is appended to the message and sent to the recipient.

3. **Verification**: The recipient uses the sender's public key to verify the signature. If the signature is valid, the recipient has reason to believe that the message was created by the sender and was not altered in transit.

## Pseudocode

The following pseudocode describes the working of the Digital Signature Standard (DSS):

```plaintext
DSS (message)
  Generate a pair of keys (private key, public key)
  Sign the message using the private key
  Verify the signature using the public key
```

## Example

### Sender side:
```bash
python3 sender.py
```

### Receiver side:
```bash
python3 receiver.py
```

### Output

Sender.py
```bash
Connected to server
Enter the message: aadityaa
P: 2221889, Q: 149, A: 14912, G: 742941
Public key: 932894
Signature[r,s]:  (10, 103)
Data:  aadityaa,10,103
Modified signature:  (678, 103)
```

Receiver.py
```bash
Connected by ('127.0.0.1', 51750)

P: 2221889

Q: 149

A: 14912

G: 742941
Received Data aadityaa,10,103
SIGNATURE:  (10, 103)
Signature verified
Received modified Data aadityaa,678,103
Modified signature not verified
```


