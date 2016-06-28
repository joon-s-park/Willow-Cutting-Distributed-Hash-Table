"""
AUTHORS: Joon Sung Park, Jacob Carstenson
DATE: 2016-4-08

"""

from node import *
from dataStructure import DataStructure
import time
from datetime import *

###########################################

class LinkedListNode(Node): 
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        ret = str(self.key) + ", " + str(self.value)
        if self.next == None:
            ret += "--||"
        else: 
            ret += "-->"
        return ret

    def getNext(self): 
        return self.next
    def getKey(self):
        return self.key
    def getValue(self):
        return self.value

    def setNext(self, n): 
        self.next = n
    def setValue(self, value):
        self.value = value

class LinkedList(DataStructure):

    def __init__(self):
        """contruct an empty linked-list"""
        self.root = None
        self.tail = None
        self.size = 0

    def __str__(self):
        ret = "(Root)"
        # get item from each node, add to ret
        curr = self.root
        for i in range(self.size):
            ret += str(curr.key) 
            ret += ", "
            ret += str(curr.value)
            
            #move curr over to next node
            curr = curr.getNext()
            if curr != None: 
                ret += "-->"
        ret += "(Tail)"
        return ret

    def put(self, key, value):
        currNode = self._objectGet(key) 
        if currNode:
            currNode.setValue(value)
        else: 
            n = LinkedListNode(key, value)
            if self.size == 0:
                self.root = n
                self.tail = n
                self.size = 1
            else:
                self.tail.setNext(n)
                self.tail = n
                self.size += 1

    # helper for put
    def _objectGet(self, key):
        curr = self.root
        for i in range(self.size):
            if curr.getKey() == key: 
                return curr
            else: 
                curr = curr.getNext()
        return None


    def get(self, key):
        curr = self.root
        for i in range(self.size):
            if curr.getKey() == key: 
                return curr.getValue()
            else: 
                curr = curr.getNext()
        return None

    def delete(self, key):
        if not self.root:
            raise KeyError('Error: key not found in tree')
        curr = self.root
        if curr.getKey() == key: 
            self.root = curr.getNext()
            self.size -= 1
        else: 
            doneFlag = False
            for i in range(self.size-2):
                if curr.getNext().getKey() == key:
                    curr.setNext(curr.getNext().getNext())
                    self.size -= 1
                    doneFlag = True
                else: 
                    curr = curr.getNext()
            if doneFlag  == False:
                if self.tail.getKey() == key:
                    self.tail = curr
                    self.tail.setNext(None)
                    size -= 1
                else: 
                    raise KeyError('Error: key not found in tree')

    def getAllNode(self):
        returnList = []
        currNode = self.root
        for i in range(self.size):
            returnList.append(currNode)
            currNode = currNode.getNext()
        return returnList


###########################################

if __name__ == "__main__":

    # LL = LinkedList()
    # print "LL INIT: ", LL
    # print "LL INIT LEN: ", len(LL) 

    # LL.put(2,"baba")
    # LL.put(3,"kaka")
    # LL.put(4,"a")
    # LL.put(5,"aska")
    # LL.put(6,"kfdka")
    # LL.put(7,"kakasdasa")
    # LL.put(8,"kakaasd")

    # LL.put(2,"new")

    # LL.delete(6)
    # LL.put(6,"kfdka")

    # print "LL NEW: ", LL
    # print "LL NEW LEN: ", len(LL)
    ht = LinkedList()
  
    x = datetime.now()
    for i in range(1000000):
        ht.put(i, i)
        print i, " is PUT"
    y = datetime.now()
    
    print "Now, 1000000 elements are in the table."
    print "This took: ", y - x