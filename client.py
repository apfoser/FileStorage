import socket
import tqdm
from _thread import *
import os

class client:
    
    def __init__(self):
        self.peers = {}
        self.files = {}
    
    '''
    Takes in ID hash
    Function returns ordered list of IP's that need to be contacted to retrieve file
    '''
    def search(id):
        return


    '''
    Takes in ordered list of IDs
    Connects to IDs and retrieves the file
    '''
    def retrieve(id_list):
        return


    '''
    Takes in a filename
    Uploads file to node network. Evenly distributes file chunks
    '''
    def put(filename):
        return 
    
    '''
    Adds self as peer to network
    '''
    def addSelf():
        return
        
        
    '''
    Takes in IP
    Adds peer to known peers list
    '''
    def addPeer(ip):
        return


#id = input("ID of your desired file: ")


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

s = socket.socket()
host = input("Host IP: ")
port = 5001
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected to ", host)
filename = input("File to Transfer: ")
filesize = os.path.getsize(filename)
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
#file = open(filename, 'wb') 

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
        
s.close()