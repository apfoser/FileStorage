import socket
import select
import tqdm
from _thread import *
import os
import threading
import time

class Node():
    
    '''
    Starts off the node in thread. 
    By default listening service is initialized in port 5001
    '''
    def __init__(self):
        self.active_peers = []
        self.peers = []
        self.sock_client = socket.socket()
        self.sock_server = socket.socket()
        self.threads = 0
        thread = threading.Thread(target = self.init_server)
        thread.start()
        
    '''
    Initializes listening service at ip:5001
    Creates service in new thread.
    Each new client gets its own threads
    '''
    def init_server(self):
        hostname = socket.gethostname()
        SERVER_HOST = socket.gethostbyname(hostname)
        SERVER_PORT = 5001
        self.sock_server.bind((SERVER_HOST, SERVER_PORT))
        self.sock_server.listen(10)
        print(f"Listening at {SERVER_HOST}:{SERVER_PORT}...")
        
        while True:
            client_socket, client_address = self.sock.accept()
            start_new_thread(self.new_client, (client_socket, client_address))
            self.peers.append(client_address[0])
            self.active_peers.append(client_address[0])
        
    '''
    Creates new thread for each additional client
    '''
    def new_client(self, socket, address):
        print(f"[+] {address} is connected.")

        socket.close()
        
    '''
    Connects to specific IP address.
    If no connection, removes from active peers
    '''
    def connect(self, address):
        self.sock_client.connect((address, 5001))
        self.sock_client.close()
        
    '''
    Updates list of active peers
    '''
    def ping_peers():
        return