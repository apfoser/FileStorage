import socket
import tqdm
from _thread import *
import os

threads = 0

hostname = socket.gethostname()
SERVER_HOST = socket.gethostbyname(hostname)
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(10)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def new_client(socket, address):
    global threads
    print(f"[+] {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    print(received)
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
            
    threads -= 1
    client_socket.close()
    
while True:
    if threads > 5:
        print("More than 5 threads, closing socket...")
        break
    else:
        client_socket, address = s.accept()
        start_new_thread(new_client, (client_socket, address))
        threads += 1
        print("Threads: " + str(threads))
    
        
s.close()