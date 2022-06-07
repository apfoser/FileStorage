import socket
import select
import string
import tqdm
from _thread import *
import os
import threading
import time
import hashlib
import sys
import pickle

# macros needed for operation
SEPARATOR = 'XXX'
# # # # # # # # # # # # # # #

class Node():
    
    '''
    Starts off the node in thread. 
    By default listening service is initialized in port 5001
    '''
    def __init__(self):
        self.active_peers = {}
        self.peers = {}
        self.threads = 0
        self.ip = ""
        self.init_client()
        self.thread_server = threading.Thread(target = self.init_server)
        self.thread_server.start()
        
    '''
    Initializes listening service at ip:5001
    Creates service in new thread.
    Each new client gets its own thread
    '''
    def init_server(self):
        self.sock_server = socket.socket()
        hostname = socket.gethostname()
        SERVER_HOST = socket.gethostbyname(hostname)
        self.ip = SERVER_HOST
        SERVER_PORT = 5001
        self.sock_server.bind((SERVER_HOST, SERVER_PORT))
        self.sock_server.listen(10)
        self.id = self.gen_id(SERVER_HOST)
        print("Node ID: " + self.id)
        print(f"Listening at {SERVER_HOST}:{SERVER_PORT}...\n")
        
        while True:
            client_socket, client_address = self.sock_server.accept()
            thread = threading.Thread(target = self.new_client, args = (client_socket, client_address))
            thread.start()
        
    '''
    Initializes client socket
    Socket is shutdown after every connection to ensure good management of ports
    '''
    def init_client(self):
        self.sock_client = socket.socket()
        self.sock_client.settimeout(.5)
        
    '''
    Creates new thread for each additional client
    '''
    def new_client(self, socket: socket, address):
        print(f"[+] {address} is connected.")
        self.peers.update({self.gen_id:address[0]})
        self.active_peers.update({self.gen_id(address[0]):address[0]})
        
        # blocking call
        received = socket.recv(11).decode('utf-8')
        if not received:
            socket.close()
            return
        
        # needed to handle any "bad" instructions sent (incomplete, etc)
        instructions = received.split(SEPARATOR)
        if len(instructions) - 1 == 0:
            mode, choice = "", ""
        else: 
            mode, choice = instructions[0], instructions[1]
        
        # choice provided to new client
        # 0x0 --> requesting data from THIS PEER
        # 0x1 --> THIS PEER will receive data
        
        # call send() or receive()
        if mode == "0x0":
            self.send(choice, address[0])
            
        elif mode == "0x1":
            self.receive(choice, socket, address[0])
        
        socket.close()
        return
        
    '''
    Generates the ID for a specific IP address
    Uses the MD5 hash
    '''
    def gen_id(self, ip):
        
        id = hashlib.md5(ip.encode('utf-8')).hexdigest()
        return id
        
    '''
    Connects to specific IP address.
    If no connection, removes from active peers
    '''
    def connect(self, address):

        id = self.gen_id(address)
        self.init_client()
        try:
            self.sock_client.connect((address, 5001))
            
        except socket.timeout:
            print("Error: Connection to node " + address + " could not be established")
            if id in self.active_peers:
                del self.active_peers[id]
            
        else:
            if id not in self.active_peers:
                self.active_peers.update({id:address})
                
    '''
    Outputs number of threads in use (ie. number of connections to node)
    '''
    def get_connections(self):
        print(threading.activeCount())
        return
        
    '''
    Updates list of active peers
    '''
    def ping_peers(self):
        #self.init_client()
        print("Updating active peers...")
        new_peers = {}
        for peer in self.active_peers:
            id = self.gen_id(self.active_peers[peer])
            self.init_client()
            try:
                self.sock_client.connect((self.active_peers[peer], 5001))
                
            except socket.timeout:
                print("Error: Connection to node " + self.active_peers[peer] + " could not be established")
                
            else:
                new_peers.update({id:self.active_peers[peer]})
            self.sock_client.close()
            
        self.active_peers = new_peers
            
            
    '''
    Prints list of active peers
    '''
    def print_peers(self):
        self.ping_peers()
        if self.active_peers:
            for peer in self.active_peers:
                print("0x" + peer + " at " + self.active_peers[peer])
        else:
            print('No active peers detected')
        return
        
    '''
    Sends text to peer
    Texts only, separate from send which handles protocol stuff
    '''
    def send_string(self, s: string):
        
        # ping peers to update active peers dictionary
        self.ping_peers()
        for peer in self.active_peers:
            self.connect(self.active_peers[peer])
            self.sock_client.send(s.encode())
            
        self.sock_client.close()
        
    
    '''
    Communicates with connected client
    Handles protocol stuff (new peer, etc)
    '''
    def send(self, choice: string, peer):
        
        self.connect(peer)
        
        # sends peer list and hash table
        if choice == "0x000":
            instruction = "0x1XXX0x000"
            self.sock_client.send(instruction.encode())
            
            # pickle peers list
            stream = pickle.dumps(self.active_peers)
            self.sock_client.send(stream)
            
        
            
        self.sock_client.close()
        return
            
    '''
    Receives data from client socket
    '''
    def receive(self, choice, socket, address):
        # receive new peer data (peers list, hash table)
        if choice == "0x000":
            received = socket.recv(1024)
            self.active_peers.update(pickle.loads(received))
        return
    
