import socket
import secrets

P = 157
alpha = 5
privatekey = secrets.randbelow(P - 1)
publickey = pow(alpha, privatekey, P)


def main():
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('localhost', 4200))
    alice_socket.listen(5)

    print("Public key of MITM", publickey)
    alice_conn, alice_addr = alice_socket.accept()

    # send my public key to alice (pretending to be bob)
    alice_conn.sendall(str(publickey).encode())

    # receive public key from alice (pretending to be bob)
    alice_publickey = int(alice_conn.recv(1024).decode())
    print("Public key of Alice", alice_publickey)

    # calculate shared secret with alice
    shared_secret_alice = pow(alice_publickey, privatekey, P)
    print("Shared Secret", shared_secret_alice)

    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.bind(('localhost', 5200))
    bob_socket.listen(5)

    bob_conn, bob_addr = bob_socket.accept()

    # send my public key to bob (pretending to be alice)
    bob_conn.sendall(str(publickey).encode())

    # receive public key from bob (pretending to be alice)
    bob_publickey = int(bob_conn.recv(1024).decode())
    print("Public key of Alice", bob_publickey)

    # calculate shared secret with alice
    shared_secret_bob = pow(bob_publickey, privatekey, P)
    print("Shared Secret", shared_secret_bob)

if __name__ == "__main__":
    main()
