import random

# Calculate the GCD of two numbers using Euclidean algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Calculate the multiplicative inverse of 'e' modulo 'phi' using Extended Euclidean algorithm
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

# Generate a prime number by generating a random 8-bit number and checking if it is prime manually
def generate_prime():
    while True:
        p = random.getrandbits(8)
        if p % 2 != 0:
            for i in range(2, p):
                if p % i == 0:
                    break
                else:
                    return p
                
# Generate a key pair (public key and private key) for RSA encryption
def generate_key_pair(p, q):
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)
    
    # Choose a random number 'e' such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    # Calculate the multiplicative inverse of 'e' modulo 'phi' to get 'd'
    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))

# Encrypt a plaintext message using the public key
def encrypt(pk, plaintext):
    key, n = pk
    # Formula: c = (message ^ pub_key) % n
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

# Decrypt a ciphertext message using the private key
def decrypt(pk, ciphertext):
    key, n = pk
    # Formula: m = (cipher ^ priv_key) % n
    plain = [chr(pow(int(chunk), key, n)) for chunk in ciphertext]
    return ''.join(plain)

if __name__ == '__main__':
    # Generate two prime numbers 'p' and 'q'
    p = generate_prime()
    q = generate_prime()
    print("P", p, "Q", q)
    
    # Generate the public key and private key pair
    public, private = generate_key_pair(p, q)
    print("Public Key", public, "Private Key", private)
    
    # Get the message from the user
    message = input("Enter Message:")
    
    # Encrypt the message using the public key
    encrypted_msg = encrypt(public, message)
    print("Encrypted Message is:", ''.join(map(lambda x: str(x), encrypted_msg)))
    
    # Decrypt the encrypted message using the private key
    print("Decrypted Message is:", decrypt(private, encrypted_msg))