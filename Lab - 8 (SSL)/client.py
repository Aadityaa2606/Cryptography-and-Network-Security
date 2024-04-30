import socket
import ssl

host = '127.0.0.1'
port = 8080
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('server.crt')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        ssock.connect((host, port))
        message = "Hello from the client!"
        ssock.sendall(message.encode())
        data = ssock.recv(1024)
        print("Received:", data.decode())



