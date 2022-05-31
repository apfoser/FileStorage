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
        self.active_peers = {}
        self.peers = {}
        self.threads = 0
        self.init_client()
        thread_server = threading.Thread(target = self.init_server)
        thread_server.start()
        
    '''
    Initializes listening service at ip:5001
    Creates service in new thread.
    Each new client gets its own threads
    '''
    def init_server(self):
        self.sock_server = socket.socket()
        hostname = socket.gethostname()
        SERVER_HOST = socket.gethostbyname(hostname)
        SERVER_PORT = 5001
        self.sock_server.bind((SERVER_HOST, SERVER_PORT))
        self.sock_server.listen(10)
        print(f"Listening at {SERVER_HOST}:{SERVER_PORT}...")
        
        while True:
            client_socket, client_address = self.sock_server.accept()
            start_new_thread(self.new_client, (client_socket, client_address))
            
    '''
    Initializes client socket
    Socket is shutdown after every connection to esnure good manegement of ports
    '''
    def init_client(self):
        self.sock_client = socket.socket()
        self.sock_client.settimeout(2)
        
        
    '''
    Creates new thread for each additional client
    '''
    def new_client(self, socket, address):
        print(f"[+] {address} is connected.")
        self.peers.update({address[0]:1})
        self.active_peers.update({address[0]:1})
        print(self.active_peers)
        
        
    '''
    Connects to specific IP address.
    If no connection, removes from active peers
    '''
    def connect(self, address):

        self.init_client()
        try:
            self.sock_client.connect((address, 5001))
            
        except socket.timeout:
            print("Error. No connection was made")
            if address in self.active_peers:
                del self.active_peers[address]
            
        else:
            if address not in self.active_peers:
                self.active_peers.update({address:1})
                
        print(self.active_peers)
        self.sock_client.close()
        
    '''
    Updates list of active peers
    '''
    def ping_peers(self):
        for peer in self.active_peers:
            self.connect(peer)
    
        return
        