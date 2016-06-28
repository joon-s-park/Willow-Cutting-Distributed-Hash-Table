"""
AUTHORS: Joon Sung Park, Jacob Carstenson
DATE: 2016-3-31

A conventional binary search implementation. The classes contained in this file include:
        1) PDBSTNode (inherited from TreeNode)
        2) PDBST (inherited from BST)

        ### LENGTH IS OFF FOR SPLITING. FIX THIS!!!
"""

from BST import *
import time
from datetime import *


class PDBSTNode(TreeNode):

    def __init__(self,key,value,left=None,right=None,parent=None, lowerBound=0, upperBound=127):
        self.key = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.lowerBound = lowerBound
        self.upperBound = upperBound


    def getMiddleBar(self):
        return ((self.upperBound - self.lowerBound)/2) + self.lowerBound 


class PDBST(BST):

    def __init__(self, lowerBound=0, upperBound=127, root=None, size=0):
        self.root = root
        self.size = size

        try:
            self.lowerBound = int(lowerBound)
            self.upperBound = int(upperBound)
        except: 
            raise ValueError('Error: Bound must be a valid integer range.')


    def put(self,key,value):
        try:
            key = int(key)
        except: 
            raise ValueError('Error: Key must be a valid integer range.')

        if key < self.lowerBound and key > self.upperBound:
            raise IndexError('Error: Key out of range.')

        if key in self:
            self.delete(key)
        if self.root: 
            self._recursivePut(key,value,self.root)
        else:
            self.root = PDBSTNode(key,value, None, None, None, self.lowerBound, self.upperBound)
        self.size += 1

    def _recursivePut(self, key, value, currentNode):
        middleBar = currentNode.getMiddleBar()
        if key <= middleBar:
            if currentNode.hasLeftChild():
                self._recursivePut(key, value, currentNode.leftChild)
            else:
                currentNode.leftChild = PDBSTNode(key, value, None, None, currentNode, currentNode.lowerBound, middleBar)

        else:
            if currentNode.hasRightChild():
                self._recursivePut(key,value,currentNode.rightChild)
            else:
                currentNode.rightChild = PDBSTNode(key, value, None, None, currentNode, middleBar+1, currentNode.upperBound)

    def get(self,key):
        if self.root:
            ret = self._recursiveGet(key,self.root)
            if ret:
                return ret.value
            else:
                return None
        else:
            return None

    def _recursiveGet(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key <= currentNode.getMiddleBar():
            return self._recursiveGet(key, currentNode.leftChild)
        else:
            return self._recursiveGet(key, currentNode.rightChild)
          
    def getLeftSubtree(self):
        middleBar = ((self.upperBound - self.lowerBound)/2) + self.lowerBound



        left_lower_bound = self.lowerBound
        left_upper_bound = middleBar

        if self.root:
            leftChild = self.root.leftChild
            return PDBST(left_lower_bound, left_upper_bound, leftChild)
        else:
            return PDBST(left_lower_bound, left_upper_bound)
            

    def getRightSubtree(self):
        middleBar = ((self.upperBound - self.lowerBound)/2) + self.lowerBound

        right_lower_bound = middleBar + 1
        right_upper_bound = self.upperBound

        if self.root:
            rightChild = self.root.rightChild
            return PDBST(right_lower_bound, right_upper_bound, rightChild)
        else:
            return PDBST(right_lower_bound, right_upper_bound)


if __name__ == "__main__":

    # currBST = PDBST(0,9)
    # # currBST[3]="red"
    # # currBST[4]="blue"
    # # currBST[6]="yellow"
    # # # currBST[2]="at"
    # # currBST[2]="attt"
    # # # currBST.delete(4)
    # # # currBST[6]="orange"
    # # currBST[7]="pink"
    # # currBST[8]="yun"
    # # currBST[9]="ye?"

    # currBST.put(3,"red")
    # currBST.put(4,"blue")
    # currBST.put(6,"yellow")
    # currBST.put(2,"attt")
    
    # currBST.put(7,"pink")
    # currBST.put(8,"yun")
    # currBST.put(9,"ye?")
   


    # currBST.delete(3)
    # currBST.delete(4)

    # print currBST




    ht = PDBST(0, 500002)

    x = datetime.now()
    for i in range(200000):
        ht.put(i, i)
        print i, " is PUT"
    y = datetime.now()
    # print ht


    print "Now, 1000000 elements are in the table."
    print "This took: ", y - x


  
