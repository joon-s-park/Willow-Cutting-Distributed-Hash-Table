import sys
sys.path.insert(0, '../')

from chainedHashTable import *
import time



print ""
print "*********************************************************************"
print "********* DEMO 3 (Part a.): 200,000 Puts in chainedHashTable ********"
print "*********************************************************************"
print ""
print "[chainedHashTable]"
print "    1) loadFactor: 0.8"
print "    2) chained data structure: BST"
print "    3) Operation Done: for i in range(200000): ht.put(i,i)"
print ""
print ""


var = raw_input("Please press any key to go on: ")



ht = ChainedHashTable(12,0.8, BST)

x = datetime.now()
for i in range(200000):
    ht.put(i,i)
    print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
print "This took: ", y - x
