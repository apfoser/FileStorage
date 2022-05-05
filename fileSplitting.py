import hashlib
import sys

from pandas import merge

'''
This program takes in a .txt file and splits it into 64kb chunks. Stores the hashes of the chunks in a Dic.
hash --> md5
chunks --> {address, hash of chunk}
storage --> {hash, data}

'''
class file:
    order = {}


# chunks of 32 bytes
BUF_SIZE = 256 

chunks = {}
storage = {}

fileSplit = file()

'''
Takes the system arguments and splits them into 32 byte chunks. 
Hashes chunks and points to address of host
'''
def split(filename):
    with open(filename, 'rb') as f:
        counter = 0
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hashed = hashlib.md5(data).hexdigest()
            if data not in chunks:
                chunks[hashed] = 1
                storage[hashed] = data
            fileSplit.order[counter] = hashed
            counter += 1
             
            
        

'''
Pieces together file, for now ignores address of host (not implemented)
File object needs to be implemented
'''
def retrieve(file):
    
    merged = b''
    
    for i in range(len(file.order)):
        merged += storage[file.order[i]]

    print(merged.decode("utf-8"))
    
    


    
                
split(sys.argv[1])
split(sys.argv[2])

print(fileSplit.order)
print(chunks)

retrieve(fileSplit)

    
    
        