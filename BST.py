"""
AUTHORS: Joon Sung Park, Jacob Carstenson
DATE: 2016-3-31

A conventional binary search implementation. The classes contained in this file include:
        1) TreeNode
        2) BST
"""

from node import *
from dataStructure import *
import time
from datetime import *
from sys import stdout
class TreeNode(Node):

    def __init__(self,key,value,left=None,right=None,parent=None):
        self.key = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def updateNodeData(self,key,value,leftChild,rightChild):
        self.key = key
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent
    
    def printPretty(self,indent, last):
        stdout.write(indent)
        if last:
            stdout.write("\\-")
            indent+=" "
        else:
            stdout.write("|-")
            indent += "| "
        stdout.write(str(self.value)+"\n")

        if self.leftChild and not self.rightChild:
            self.leftChild.printPretty(indent, 1)
        elif not self.leftChild and self.rightChild:
            self.rightChild.printPretty(indent, 1)
        elif self.leftChild and self.rightChild:
            self.leftChild.printPretty(indent, 0)
            self.rightChild.printPretty(indent, 1)
        elif not self.leftChild and not self.rightChild:
            pass

class BST(DataStructure):

    def __init__(self):
        self.root = None
        self.size = 0

    def traverseLevelOrder(self):
        thisLevel = [self.root]
        while not all(v is None for v in thisLevel):
            nextLevel = []
            for n in thisLevel:
                if n:
                    print n.value,
                    if n.leftChild: 
                        nextLevel.append(n.leftChild)
                    else:
                        nextLevel.append(None)
                    if n.rightChild: 
                        nextLevel.append(n.rightChild)
                    else:
                        nextLevel.append(n.rightChild)
                else:
                    print "NONE",
            print
            thisLevel = nextLevel


    def traverseInorderToList(self, node):
        currList = []
        self._traverseInorder(node, currList)
        return currList

    def _traverseInorder(self, node, currList):
        if node:
            self._traverseInorder(node.hasLeftChild(),currList)
            currList.append(node.value)
            self._traverseInorder(node.hasRightChild(),currList)

    def _objectTraverseInorderToList(self, node):
        currList = []
        self._objectTraverseInorder(node, currList)
        return currList

    def _objectTraverseInorder(self, node, currList):
        if node:
            self._objectTraverseInorder(node.hasLeftChild(),currList)
            currList.append(node)
            self._objectTraverseInorder(node.hasRightChild(),currList)        

    # Uses "traverseLevelOrder" convention

    

    def __str__(self):
        #self.traverseLevelOrder()
        if self.root:
            self.root.printPretty("",1)
        else:
            print "Empty tree"
        return "\n"

    def put(self,key,value):
        if key in self:
            self.delete(key)
        if self.root:
            self._recursivePut(key,value,self.root)
        else:
            self.root = TreeNode(key,value)
        self.size = self.size + 1

    def _recursivePut(self,key,value,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._recursivePut(key,value,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,value,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._recursivePut(key,value,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,value,parent=currentNode)

    def get(self,key):
        if self.root:
            ret = self._recursiveGet(key,self.root)
            if ret:
                return ret.value
            else:
                return None
        else:
            return None

    def _objectGet(self, key):
        if self.root:
            ret = self._recursiveGet(key,self.root)
            if ret:
                return ret
            else:
                return None
        else:
            return None

    def _recursiveGet(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._recursiveGet(key,currentNode.leftChild)
        else:
            return self._recursiveGet(key,currentNode.rightChild)

    def delete(self,key):
        if self.size > 1:
            nodeToRemove = self._recursiveGet(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
            else:
                raise KeyError('Error: key not found in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error: key not found in tree')

    def remove(self,currentNode):
        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): #interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.value = succ.value

        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.updateNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.value,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.updateNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.value,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)

    def getAllNode(self):
        return self._objectTraverseInorderToList(self.root)



if __name__ == "__main__":
    

    # currBST = BST()
    # currBST[3]="red"
    # currBST[4]="blue"
    # currBST[6]="yellow"
    # currBST[2]="at"
    # currBST[2]="attt"
    # currBST.delete(4)
    # currBST[6]="orange"
    # currBST[7]="pink"
    # currBST[8]="yun"
    # currBST[9]="ye?"

    # currBST.delete(3)



    # print currBST


    ht = BST()

    x = datetime.now()
    for i in range(1000):
        ht.put(i, i)
        print i, " is PUT"
    y = datetime.now()
    
    print "Now, 1000000 elements are in the table."
    print "This took: ", y - x

