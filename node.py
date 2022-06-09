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
import re
import random


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
        self.chunks = {}
        self.files = {}
        self.buf = b''
        self.threads = 0
        self.ip = ""
        self.recv = False
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
        self.active_peers.update({self.gen_id(self.ip):self.ip})
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
        #print(f"[+] {address} is connected.")
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
            if choice == "0x010":
                hash = socket.recv(32)
            self.send(choice, address[0], hash = hash)
            
        elif mode == "0x1":
            self.recv = True
            self.receive(choice, socket, address[0])
            
            
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
        
        rgx = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
       
        if(not re.search(rgx, address)):
            
            print("Invalid address")
            return

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
    Send request to peer
    Different with send() function in that it doesn't handle any objects
    Just text aka system requests
    '''
    def send_request(self, s: string, peer, hash = ""):
           
        self.connect(peer)
        
        msg = s + hash
        self.sock_client.send(msg.encode())
            
        self.sock_client.close()
        
    
    '''
    Communicates with connected client
    Handles protocol stuff (new peer, etc)
    '''
    def send(self, choice: string, peer, dat = "", hash = ""):
        
        self.connect(peer)
        
        # sends peer list and hash table
        if choice == "0x000":
            instruction = "0x1XXX0x000"
            self.sock_client.send(instruction.encode())
            
            # pickle peers list
            stream = pickle.dumps(self.active_peers)
            
            # sending size of byte stream
            size = len(stream)
            size_msg = (4-len(str(size)))*"0" + str(size)
            
            self.sock_client.send(size_msg.encode())
            
            # send pickled object
            self.sock_client.send(stream)
            
        # sends file to peer
        # used by put_file method 
        # splitting only (PUT)   
        elif choice == "0x001":
            
            instruction = "0x1XXX0x001"
            self.sock_client.send(instruction.encode())
            
            size = len(dat)
            size_msg = (4-len(str(size)))*"0" + str(size)
            
            self.sock_client.send(size_msg.encode())
            self.sock_client.send(dat)
            
        elif choice == "0x010":
            
            instruction = "0x1XXX0x010"
            self.sock_client.send(instruction.encode())
            
            test_text = 'test text'
            self.sock_client.send(test_text.encode())
            
        self.sock_client.close()
        return
            
    '''
    Receives data from client socket
    '''
    def receive(self, choice, socket, address):
        # receive new peer data (peers list, hash table)
        if choice == "0x000":
            size = int(socket.recv(4))
            received = socket.recv(size)
            print(pickle.loads(received))
            self.active_peers.update(pickle.loads(received))
            
        # receives file from peer
        # splitting only (PUT)
        elif choice == "0x001":
            size = int(socket.recv(4))
            received = socket.recv(size)
            
            chunk_hash = hashlib.md5(received).hexdigest()
            filename = chunk_hash
            self.chunks.update({chunk_hash:filename})
            with open(chunk_hash, "wb") as f:
                f.write(received)
            
        elif choice == "0x010":
            
            rec = socket.recv(9)
            print(rec)
            
            
        self.recv = False
        return
    
    '''
    Put file into system
    '''
    def put_file(self, filename, chunksize):
        
        file_order = []
        filesize = os.path.getsize(filename)
        
        # buggy output, commented out for now
        #progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        
        with open(filename, 'rb') as f:
            h = hashlib.md5()
            
            while True:
                dat = f.read(chunksize)
                #progress.update(len(dat))
                if not dat:
                    break
                
                h.update(dat)
                chunk_hash = hashlib.md5(dat).hexdigest()
                peer = random.choice(list(self.active_peers.values()))
                
                self.send("0x001", peer, dat)
                
                file_order.append((chunk_hash, peer))
                
            file_hash = h.hexdigest()
            # sleep needed otherwise progress bar is messed up
            self.files.update({file_hash:file_order})
            print("File hash: " + file_hash)
            # print(self.files[file_hash])
            
    '''
    Gets file from system
    '''
    def retrieve(self, file_hash):
        
        print(self.files[file_hash])
        for pair in self.files[file_hash]:
            
            self.send_request(hash = pair[0], peer = pair[1], s = "0x0XXX0x010")
            
            
        return