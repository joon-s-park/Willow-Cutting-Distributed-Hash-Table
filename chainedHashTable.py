from dataStructure import *
from linkedList import *
from BST import *
from node import *
import time
from datetime import *

class ChainedHashTable(DataStructure):
    
    def __init__(self, initialCapacity=12, loadFactor=0.8, chainedDataStructure=LinkedList):
        self.size = 0
        self.capacity = initialCapacity
        self.loadFactor = loadFactor
        self.chainedDataStructure = chainedDataStructure
        self.buckets = [self.capacity]
        self.buckets = [chainedDataStructure() for i in range(self.capacity)]

    def __str__(self):
        ret = ""
        for i,b in enumerate(self.buckets):
            ret += "Bucket %d" % i
            ret += b.__str__()
            ret += ""
        return ret

    def hash(self, key):
        if str(key).isdigit():
            ret = key % self.capacity
            if ret < 0:
                ret += self.capacity
            return ret
        else: 
            total = 0
            for i in range(len(key)):
                total = 31*total + ord(key[i])
            ret = total % self.capacity
            if ret < 0:
                ret += self.capacity
            return ret

    def expandCapacity(self): 
        oldCapacity = self.capacity
        self.capacity = self.capacity * 2

        tempBuckets = [self.capacity]
        tempBuckets = [self.chainedDataStructure() for i in range(self.capacity)]

        for i in range(oldCapacity):
            if self.buckets[i]:
                allNode = self.buckets[i].getAllNode()
                for j in allNode:
                    newHashedIndex = self.hash(j.getKey())
                    tempBuckets[newHashedIndex].put(j.getKey(), j.getValue())

        self.buckets = tempBuckets

    def hashOverload(self): 
        currentLoad = (self.size+1)/float(self.capacity)

        if (currentLoad > self.loadFactor):
            return True
        else: 
            return False

    def put(self, key, value):
        if self.hashOverload(): 
            # print "expand"
            self.expandCapacity()
            # print "expand DONE"


        hashedIndex = self.hash(key)
        currNode = self.buckets[hashedIndex]._objectGet(key)

        if currNode != None:
            currNode.setValue(value)
       
        self.buckets[hashedIndex].put(key, value)
        self.size += 1

    def get(self, key):
        hashedIndex = self.hash(key)
        
        return self.buckets[hashedIndex].get(key)

    def delete(self, key):
        hashedIndex = self.hash(key)

        self.buckets[hashedIndex].delete(key)
        self.size -= 1

    def getAllNode(self):
    	ret = []
    	for i in self.buckets:
            innerList = i.getAllNode()
            for j in innerList:
            	ret.append(j)

        return ret
if __name__ == "__main__":

    # ht = ChainedHashTable(12, 0.8, BST)

    # print ht

    # ht.put(1, "a")
    # ht.put(2, "a")
    # ht.put(3, "a")
    # ht.put(4, "a")
    # ht.put(5, "a")
    # ht.put(6, "a")
    # ht.put(7, "a")
    # ht.put(8, "a")
    # ht.put(9, "a")
    # ht.put(10, "a")

    # ht.put(11, "a")
    # ht.put(12, "a")
    # ht.put(13, "a")
    # ht.put(14, "a")
    # ht.put(15, "a")
    # ht.put(16, "a")

    # ht.put(17, "a")
    # ht.put(18, "a")
    # ht.put(19, "a")
    # ht.put(20, "a")

    # # x = ht.getAllNode()
    # # for i in x: 
    # # 	print i

    # print ht.get(17)
    # ht.delete(19)
    # print ht.get(19)

    ht = ChainedHashTable(12,0.8, BST)

    x = datetime.now()
    for i in range(200000):
        ht.put(i,i)
        #print i, " is PUT"
    y = datetime.now()

    print "Now, 1000000 elements are in the table."
    print "This took: ", y - x

    # time.sleep(3)


    
    # print "We will now expand ten times."
    
    # x = datetime.now()
    # for i in range(10):
    #     print "expand"
    #     ht.expandCapacity()
    #     print "DONE"
    # y = datetime.now()

    # print "This took: ", y - x

    # for i in range(1000, 1000000):
    #     print ht.get(i)

    # x = datetime.now()
    # for i in range(500000):
    #     print ht.get(i)
    # y = datetime.now()

    # print "Now, we got 1000000 elements."
    # print "This took: ", y - x
