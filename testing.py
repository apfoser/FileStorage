import node
import time

print("Python P2P File Sharing")
print("-----------------------\n")

node = node.Node()

time.sleep(.1)

while True:
    choice = input("Enter command: ")
    
    if choice == "connect":
        ip = input("IP address: ")
        node.connect(ip)
        
    if choice == "exit":
        node.exit()
        
    if choice == "peers":
        node.ping_peers()
        