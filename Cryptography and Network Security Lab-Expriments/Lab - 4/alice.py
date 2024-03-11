import socket
import secrets

P = 157
alpha = 5


def sender():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 4200))

        privatekey = secrets.randbelow(P - 1)
        publickey = pow(alpha, privatekey, P)

        print("Generated Public Key", publickey)

        # sending public key to bob
        s.sendall(str(publickey).encode())
        bobpubkey = int(s.recv(1024).decode())
        shared_secret_bob = pow(bobpubkey, privatekey, P)
        print("Shared Secret with Bob", shared_secret_bob)

        # sending shared secret to bob
        s.sendall(str(shared_secret_bob).encode())


if __name__ == '__main__':
    sender()