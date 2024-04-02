import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

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

def generate_prime():
    # Generates a prime number by generating a random 10 bit number and checking if it is prime manually
    while True:
        p = random.getrandbits(8)
        if p % 2 != 0:
            for i in range(2, p):
                if p % i == 0:
                    break
                else:
                    return p
                
def generate_key_pair(p, q):
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    # Decrypt each chunk
    plain = [chr(pow(int(chunk), key, n)) for chunk in ciphertext]
    return ''.join(plain)

if __name__ == '__main__':
    p = generate_prime()
    q = generate_prime()
    print("P", p, "Q", q)
    public, private = generate_key_pair(p, q)
    print("Public Key", public, "Private Key", private)
    message = input("Enter Message:")
    encrypted_msg = encrypt(public, message)
    print("Encrypted Message is:", ''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypted Message is:", decrypt(private, encrypted_msg))