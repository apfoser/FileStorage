import node
import time

node = node.Node()

node.connect('192.168.1.219')


time.sleep(10)

print("starting again")

node.connect('192.168.1.219')