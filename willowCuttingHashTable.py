from PDBST import *
from dataStructure import *
from linkedList import *
from BST import *
from node import *
from chainedHashTable import *
import math
import time
from datetime import *

class WillowCuttingHashTable(ChainedHashTable):

    def __init__(self, loadFactor, lowerBound, upperBound, initialCapacity=12):
        self.size = 0
        self.capacity = initialCapacity
        self.loadFactor = loadFactor
        self.chainedDataStructure = PDBST
        
        self.global_lower = lowerBound
        self.global_upper = upperBound

        self.lowerBound = lowerBound
        self.upperBound = upperBound

        self.buckets = []

        allBounds = self.upperBound - self.lowerBound + 1
        step = float(allBounds)/self.capacity

        self.buckets = [PDBST(self.lowerBound + round((i*step)), self.lowerBound + round((i+1)*step)-1) for i in range(self.capacity)]
        self.buckets[-1].upperBound = self.upperBound


        # for i in range(self.capacity):
        #     if i == 0:
        #         self.buckets.append(PDBST(self.lowerBound, self.lowerBound + round(step) - 1))
        #     else:
        #         currOffset = self.lowerBound + round(i*step)
        #         currEnd = self.lowerBound + round((i+1)*step) - 1
        #         if currEnd > self.upperBound:
        #             currEnd = self.upperBound
        #         elif i == self.capacity-1 and currEnd < self.upperBound:
        #             currEnd = self.upperBound
        #         self.buckets.append(PDBST(currOffset, currEnd))

        self.lowerbounds = [round(i*step)+self.lowerBound for i in range(self.capacity)]
        self.upperbounds = [round((i+1)*step)-1+self.lowerBound for i in range(self.capacity)]


        # for i in range(self.capacity):
        #     if i == 0:
        #         self.buckets.append(PDBST(self.lowerBound, self.lowerBound+round(step)-1))
        #     else: 
        #         currOffset = self.buckets[i - 1].upperBound + 1
        #         currEnd = currOffset + round(step) - 1
        #         if currEnd > self.upperBound:
        #             currEnd = self.upperBound
        #         elif i == self.capacity-1 and currEnd < self.upperBound:
        #             currEnd = self.upperbound
        #         self.buckets.append(PDBST(currOffset, currEnd))


    def hash(self, key):
        if str(key).isdigit() and (key >= self.global_lower and key <= self.global_upper):
            allBounds = self.global_upper - self.global_lower + 1
            ret = (key * 4561) % allBounds
            ret += self.global_lower
            return ret
        else: 
            raise ValueError("THE KEY MUST BE AN INTEGER WITHIN THE RANGE")
    def _unboundedHash(self, key):
        if str(key).isdigit():
            allBounds = self.global_upper - self.global_lower + 1
            ret = (key * 4561) % allBounds
            ret += self.global_lower
            return ret
            #return key
        else:
            raise ValueError("THE KEY MUST BE AN INTEGER")
        
    def expandCapacity(self):
        oldCapacity = self.capacity
        self.capacity = self.capacity * 2

        tempBuckets = []



        for i,tree in enumerate(self.buckets):
            tempBuckets.append(tree.getLeftSubtree())
            tempBuckets.append(tree.getRightSubtree())
            
            if tree.getRootNode():

                hashed_key = tree.getRootNode().key

                if hashed_key > tempBuckets[i*2].upperBound:
                    tempBuckets[i*2+1].put(tree.getRootNode().key, tree.getRootNode().value)
                else:
                    tempBuckets[i*2].put(tree.getRootNode().key, tree.getRootNode().value)

        self.buckets = tempBuckets


        self.lowerbounds = []
        self.upperbounds = []
        for i in range(self.capacity):
            self.lowerbounds.append(self.buckets[i].lowerBound)
            self.upperbounds.append(self.buckets[i].upperBound)


    def put(self, key, value):
        

        
        if self.hashOverload(): 
            # print self.hashOverload(), "HASH OVERLOAD?"
            # print self.size, "size"
            print "expand"


            self.expandCapacity()
            print "expand DONE"
    
        hashedIndex = self.hash(key)
        bucketIndex = self._getBucketIndex(hashedIndex)
        
        currNode = self.buckets[bucketIndex]._objectGet(hashedIndex)

        if currNode != None:
            currNode.setValue(value)
       
        else:
            self.buckets[bucketIndex].put(hashedIndex, value)
            self.size += 1

    def get(self, key):
        hashedIndex = self.hash(key)
        bucketIndex = self._getBucketIndex(hashedIndex)
        
        return self.buckets[bucketIndex].get(hashedIndex)

    def delete(self, key):
        hashedIndex = self.hash(key)
        bucketIndex = self._getBucketIndex(hashedIndex)

        self.buckets[bucketIndex].delete(hashedIndex)
        self.size -= 1

    def _getBucketIndex(self, hashedKey):
        for i in range(self.capacity):
            if hashedKey <= self.upperbounds[i] and hashedKey >= self.lowerbounds[i]:
                return i

    def splitTable(self, index):
        left_upper = self.buckets[index-1].upperBound
        leftHT = WillowCuttingHashTable(self.loadFactor, self.lowerBound, left_upper, index)

        right_lower = self.buckets[index].lowerBound
        right_capacity = self.capacity - index
        rightHT = WillowCuttingHashTable(self.loadFactor, right_lower, self.upperBound, right_capacity)

        for i in range(self.capacity):
            if i < index:
                leftHT.buckets[i] = self.buckets[i]
            else:
                rightHT.buckets[i-index] = self.buckets[i]

        leftHT.global_lower = self.global_lower
        leftHT.global_upper = self.global_upper
        rightHT.global_lower = self.global_lower
        rightHT.global_upper = self.global_upper

        return leftHT, rightHT



if __name__ == "__main__":

    # ht = WillowCuttingHashTable(0.8, 0, 50)

    # num = 51


    # for i in range(num):
    #     char = chr(ord('a') + i)
    #     ht.put(i, char)


    # x = ht.getAllNode()
    # for i in x: 
    #   print i

    # print ""

    # for i in range(num):
    #     print "get ",i
    #     print ht.get(i)

    # print "BUCKETS"

    # for i in range(ht.capacity):
    #     print "pdbst ",i
    #     print ht.buckets[i]

    # print "lower bounds: ",ht.lowerbounds
    # print "upper bounds: ",ht.upperbounds


    # ht.delete(19)
    # print "getting 19: ",ht.get(19)

    # for i in range(50):
    #     print i
    #     ht.put(i, "%d" % i)
    # for i in range(50):
    #     ht.get(i)

    ht = WillowCuttingHashTable(1000, 0, 500000)


    x = datetime.now()
    for i in range(200000):
    	ht.put(i, i)
    	#print i, " is PUT"
    y = datetime.now()
    
    print "Now, 1000000 elements are in the table."
    print "This took: ", y - x

    # left_ht, right_ht = ht.splitTable(ht.capacity/4)

    # print "Left node contents: ", len(left_ht)

    # x = left_ht.getAllNode()
    # for i in x: 
    #   print i

    # print "\n\n Right Node contents: ", len(right_ht)

    # x = right_ht.getAllNode()
    # for i in x: 
    #   print i


    # time.sleep(3)

    # print "We will now expand ten times."

    # x = datetime.now()
    # for i in range(15):
    # 	print "expand"
    #     ht.expandCapacity()
    #     print "DONE"
    # y = datetime.now()

    # print "This took: ", y - x


    # x = datetime.now()
    # for i in range(500000):
    # 	print ht.get(i)
    # y = datetime.now()
    # print "Now, we got 500000 elements."
    # print "This took: ", y - x


    # ht = ChainedHashTable(12,0.8, BST)

    # x = datetime.now()
    # for i in range(1000000):
    #     ht.put(i,i)
    #     print i, " is PUT"
    # y = datetime.now()

    # print "Now, 1000000 elements are in the table."
    # print "This took: ", y - x
