import sys
sys.path.insert(0, '../')

from BST import *
import time



print ""
print "*********************************************************************"
print "**************** DEMO 2 (Part a.): 1000 Puts in BST *****************"
print "*********************************************************************"
print ""
print ""
print "    Operation Done: for i in range(1000): bst.put(i,i)"
print ""
print ""


var = raw_input("Please press any key to go on: ")




ht = BST()

for i in range(1000):
    ht.put(i, i)
