import node
import time
import os

print("\nPython P2P File Sharing by apfoser")
print("----------------------------------")

node = node.Node()

while True:
    choice = input("")
    
    if choice == "connect":
        ip = input("IP address: ")
        if ip == "self":
            ip = node.ip
        node.connect(ip)
        
    elif choice == "exit":
        node.exit()
        
    elif choice == "peers":
        node.ping_peers()
        
    elif choice == "print peers":
        node.print_peers()
        
    elif choice == "send":
        s = input("request: ")
        peer = input("ip of peer: ")
        node.send_request(s, peer)
        
    elif choice == "connections":
        node.get_connections()
    
    elif choice == "clear":
        os.system('cls')
        
    elif choice == "put":
        filename = input("filename: ")
        node.put_file(filename, 8)
        
    elif choice == "get":
        id = input("File Hash: ")
        node.retrieve(id)