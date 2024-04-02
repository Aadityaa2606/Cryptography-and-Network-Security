import socket
import json
from gmpy2 import invert

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if ((a*x) % m == 1):
            return (x)
    return (1)

def verify(message, r, s, p, q, g):
    # w = pow(s, -1, q)
    w = invert(s, q)

    u1 = (message * w) % q
    u2 = (r * w) % q

    checkpoint = ((pow(g, u1)* pow(pub_key, u2)) % p) % q

    print(f"Intermediate vals:\nw = {w}\nu1 = {u1}\nu2 = {u2}\nv = {checkpoint}\n")

    if checkpoint == r: return 'Signature verified'
    return 'Signature not verified'


def flow_handler(message, r, s, p, q, g):

    print(f"Recived message: {message}\n(r,s) = {r}, {s}\n(p, q) = {p}, {q}\ng = {g}\n")

    result = verify(message, r, s, p, q, g)

    print(result)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        ss.bind(('localhost', 8080))
        ss.listen()

        print("Waiting for connection...")
        conn, addr = ss.accept()
        print("Connected to", addr)
        print('\n')

        with conn:
            data = conn.recv(1024).decode()  # Receive data from sender
            received_data = json.loads(data)  # Deserialize JSON data

            r = int(received_data["r"])
            s = int(received_data["s"])
            pub_key = int(received_data["pub_key"])
            p = int(received_data["p"])
            q = int(received_data["q"])
            g = int(received_data["g"])
            hashed_message = int(received_data["hashed_message"])

            flow_handler(hashed_message, r, s, p, q, g)

            # mod_mes = input("Enter modified message: ")

            # flow_handler(mod_mes, r, s, p, q, g)








