import socket
import sys
import os
from threading import Thread
import time

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request_data):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    client_socket.send(request_data)
    # Shutdown not actually needed for google but good in general
    client_socket.shutdown(socket.SHUT_WR)

    data = client_socket.recv(BYTES_TO_READ)
    result = b'' + data
    while(len(data) > 0):
      data = client_socket.recv(BYTES_TO_READ)
      result += data
    
    return result

def handle_connection(conn, addr):
  with conn:
    print(f"Connected to by: {addr}")

    # Accumulate request data
    request = b''
    while True:
      data = conn.recv(BYTES_TO_READ)
      if not data: break
      print(data)
      request += data
    
    # Forward request to google
    response = send_request("www.google.com", 80, request)
    # print(response)
    
    # Send data back to client
    conn.sendall(response)

def start_server():

  while True:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.listen(2)  # Arguement tells socket how many requests to queue

      conn, addr = server_socket.accept()

      pid = os.fork()

      if pid > 0:
        # Child
        handle_connection(conn, addr)
        return

def start_threaded_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.listen(2)  # Arguement tells socket how many requests to queue

      while True:
        conn, addr = server_socket.accept()
        thread = Thread(target=handle_connection, args=(conn, addr))
        thread.run()

def start_forked_server():

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(2)  # Arguement tells socket how many requests to queue

    while True:
      conn, addr = server_socket.accept()

      pid = os.fork()
      print(pid)

      if pid == 0:
        # Child
        handle_connection(conn, addr)
        time.sleep(20)
        os._exit(0)
      
      # Parent
      conn.close()
  
# start_server()
# start_threaded_server()
start_forked_server()