import socket
import ssl

host = '127.0.0.1'
port = 8080
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('server.crt', 'server.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((host, port))
    sock.listen()
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Received:", data.decode())
                conn.sendall(data)
