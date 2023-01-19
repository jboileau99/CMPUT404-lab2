import socket

# Connect to www.google.com and request a page
HOST = 'www.google.com'
PORT = 80
BYTES_TO_READ = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'GET http://www.google.com/ HTTP/1.1\nHost:' + HOST.encode('utf-8') + b'\n\n')
    s.shutdown(socket.SHUT_WR)
    data = s.recv(1024)

    # Get and print entire response
    full_response = b''
    response = s.recv(BYTES_TO_READ)
    while(len(response) > 0):
        full_response += response
        response = s.recv(BYTES_TO_READ)
    print(full_response)