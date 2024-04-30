import socket
import random
import string
import hashlib
from sympy import isprime

def generate_random_prime():
    """Generate a random prime number"""
    candidate = 0
    while True:
        candidate = random.getrandbits(24)
        if isprime(candidate):
            break
    return candidate

def generate_public_values():
    # generate p and q and also check if p-1 is divisible by q
    p = generate_random_prime()
    # find q such that p-1 is divisible by q and q is prime
    q = generate_random_prime()
    while (p-1) % q != 0:
        q = generate_random_prime()
    while True:
        # generate value of h
        a = int((p - 1) // q)
        h = random.randint(2, p-2)
        g = pow(h, a, p)
        if g != 1:
            break
    return (p, q, a, g)

def find_hash(m: string, q: int):
    # to bytes
    m = str.encode(m)
    hash_value = hashlib.sha1(m).digest()
    # Convert the hash value to an integer
    return int.from_bytes(hash_value, 'big') % q

def sign(q, p, g, x, H):
    k = random.randint(1, q-1)

    r = pow(g, k, p) % q
    s = (pow(k, -1, q) * (H + x * r)) % q
    return (r, s)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    print('Connected to server')
    # get the message from the user
    message = input('Enter the message: ')
    # generate public values
    (p, q, a, g) = generate_public_values()
    # generate public values
    print("P: %d, Q: %d, A: %d, G: %d" % (p, q, a, g))
    # generate keys
    private_key = random.randint(1, q-1)
    public_key = pow(g, private_key, p)
    print("Public key: %d" % public_key)
    pub = str(p)+","+str(q)+","+str(a)+","+str(g)+","+str(public_key)
    # send the public values to the server
    s.sendall(pub.encode('utf-8'))
    # find the hash
    hash_value = find_hash(message, q)
    # sign the message
    signature = sign(q, p, g, private_key, hash_value)
    print('Signature[r,s]: ', signature)
    data = message + "," + str(signature[0]) + "," + str(signature[1])
    print('Data: ', data)
    # send the message and signature to the server
    s.sendall(data.encode('utf-8'))
    # modify the signature slightly
    from time import sleep
    sleep(2)
    signature = (signature[0] + random.randint(1, 1000), signature[1])
    print('Modified signature: ', signature)
    # try to verify the signature again
    data = message + "," + str(signature[0]) + "," + str(signature[1])
    s.sendall(data.encode('utf-8'))
