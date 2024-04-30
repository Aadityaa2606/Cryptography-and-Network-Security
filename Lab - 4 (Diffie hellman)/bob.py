import socket
import secrets

P = 157
alpha = 5

def receiver():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5200))

        privatekey = secrets.randbelow(P - 1)
        publickey = pow(alpha, privatekey, P)

        print("Generated Public Key", publickey)

        # sending public key to alice
        s.sendall(str(publickey).encode())
        alicepubkey = int(s.recv(1024).decode())
        alice_secret_bob = pow(alicepubkey, privatekey, P)
        print("Shared Secret with Alice", alice_secret_bob)

        # sending shared secret to alice
        s.sendall(str(alice_secret_bob).encode())

if __name__ == '__main__':
    receiver()