import socket

# Connect to www.google.com and request a page
HOST = '127.0.0.1'
PORT = 80
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'GET http://www.google.com/ HTTP/1.1\n\n')
    data = s.recv(1024)
print(f'Received from {HOST}:\n\n', repr(data))