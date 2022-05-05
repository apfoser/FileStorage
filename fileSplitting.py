import hashlib
import sys
'''
This program takes in a .txt file and splits it into 64kb chunks. Stores the hashes of the chunks in a Dic.
hash --> md5
chunks --> {address, hash of chunk}
storage --> {hash, data}

'''

# chunks of 32 bytes
BUF_SIZE = 256 

chunks = {}
storage = {}

class file:
    
    def __init__(self, filename):
        self.filename = filename
        self.order = {}
    
    def split(self):
        with open(self.filename, 'rb') as f:
            counter = 0
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                hashed = hashlib.md5(data).hexdigest()
                if data not in chunks:
                    chunks[hashed] = 1
                    storage[hashed] = data
                self.order[counter] = hashed
                counter += 1
                
        # print(chunks)
    


'''
Pieces together file, for now ignores address of host (not implemented)
File object needs to be implemented
'''
def retrieve(file):
    merged = b''
    for i in range(len(file.order)):
        merged += storage[file.order[i]]

    #print(len(merged.decode("utf-8")))
    return len(merged.decode("utf-8"))
    
    
    
# some testing (seems to work!)
fileA = file(sys.argv[1])
fileB = file(sys.argv[2])

fileA.split()
fileB.split()

#retrieve(fileA)
#retrieve(fileB)

# number of chars outputed
total = retrieve(fileA) + retrieve(fileB)

m = b''
for each in storage:
    m += storage[each]
    
# number of chars actually stored
stored = len(m.decode('utf-8'))

print("storage savings of " + str(100*(total - stored)/total) + "%")
    
    
        