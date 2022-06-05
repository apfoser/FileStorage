import node
import time
import threading

print("\nPython P2P File Sharing by apfoser")
print("----------------------------------")

node = node.Node()

time.sleep(.1)

while True:
    choice = input("")
    
    if choice == "connect":
        ip = input("IP address: ")
        node.connect(ip)
        
    if choice == "exit":
        node.exit()
        
    if choice == "peers":
        node.ping_peers()
        
    if choice == "print peers":
        node.print_peers()
        
    if choice == "send":
        node.send("test test test test")
        
    if choice == "connections":
        node.get_connections()
    