import socket

# Connect to www.google.com and request a page
GOOGLE_HOST = 'www.google.com'
GOOGLE_PORT = 80

PROXY_HOST = ''
PROXY_PORT = 8001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Bind to host and port
    s.bind((PROXY_HOST, PROXY_PORT))

    # Continually accept new connections
    while(True):
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connection from:', addr)
            while True:
                # Echo back whatever data is received
                data = conn.recv(1024)
                print(data)
                if not data: break
                conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((GOOGLE_HOST, GOOGLE_PORT))
    s.sendall(b'GET http://www.google.com/ HTTP/1.1\n\n')
    data = s.recv(1024)
print(f'Received from {GOOGLE_HOST}:\n\n', repr(data))