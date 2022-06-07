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
        
    if choice == "exit":
        node.exit()
        
    if choice == "peers":
        node.ping_peers()
        
    if choice == "print peers":
        node.print_peers()
        
    if choice == "send":
        s = input("request: ")
        peer = input("ip of peer: ")
        node.send_request(s, peer)
        
    if choice == "connections":
        node.get_connections()
    
    if choice == "clear":
        os.system('cls')
        