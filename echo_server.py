import socket

HOST = ''
PORT = 8001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Bind to host and port
    s.bind((HOST, PORT))

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