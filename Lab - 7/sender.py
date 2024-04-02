import socket
import random
import json
import hashlib

def is_prime(n, k=5):
    """Test if a number is prime using Miller-Rabin primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as d*2^r + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test for 'k' rounds
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=40):
    """Generate a random prime number with 'bits' bits."""
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

p, q = (generate_prime(),  generate_prime())

def key_gens():
    a = (p-1) // q
    h = random.randint(2, p-2)
    g = pow(h, a, p)

    # private key 
    pvt_key = random.randint(1, q-1)

    # public key: g^pvt_key mod p
    pub_key = pow(g, pvt_key, p)

    return pub_key, pvt_key, g


def signing_message(hashed_message, g, pvt_key):
    k = random.randint(1, q-1)

    # (g^k mod p) % q 
    r = pow(g, k, p) % q

    s = (pow(k, -1, q) * (hashed_message + pvt_key * r)) % q

    return (r, s)

def find_hash(message, q):
    # to bytes
    message = str.encode(message)
    hash_value = hashlib.sha1(message).digest()
    # Convert the hash value to an integer
    return int.from_bytes(hash_value, 'big') % q


def flow_handler(message):

    print(f"\n(p,q) = {p}, {q}")

    hashed_message = find_hash(message, q)

    print(f"\nHashed message = {hashed_message}\n")

    pub_key, pvt_key, g = key_gens()

    print(f"(Pub key, Pvt key): {pub_key}, {pvt_key}\n")

    print(f"g = {g}\n")

    r, s = signing_message(hashed_message, g, pvt_key)

    print(f"(r,s) = {r}, {s}")

    # hashed_message, (r,s), public key, q, p ->sent to receiver
    return hashed_message, (r,s), pub_key, p, q, g


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.connect(('localhost', 8080))

        print("Connected to server!\n")

        message = input("Enter the message: ")

        hashed_message, (r, s), pub_key, p, q, g = flow_handler(message)

        data = {
            "r": str(r),
            "s": str(s),
            "pub_key": str(pub_key),
            "p": str(p),
            "q": str(q),
            "g": str(g),
            "hashed_message": str(hashed_message)
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(data)

        # Send the JSON data over the socket connection
        ss.send(json_data.encode())



