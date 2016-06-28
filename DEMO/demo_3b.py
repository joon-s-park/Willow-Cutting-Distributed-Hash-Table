import sys
sys.path.insert(0, '../')

from willowCuttingHashTable import *
import time



print ""
print "*********************************************************************"
print "****** DEMO 3 (Part b.): 200,000 Puts in willowCuttingHashTable *****"
print "*********************************************************************"
print ""
print "[willowCuttingHashTable]"
print "    1) loadFactor: 1000"
print "    2) chained data structure: PDBST"
print "    3) range: 0 to 10000001"
print "    4) Operation Done: for i in range(200000): ht.put(i,i)"
print ""
print ""


var = raw_input("Please press any key to go on: ")



ht = WillowCuttingHashTable(1000, 0, 10000001)

x = datetime.now()
for i in range(200000):
	ht.put(i, i)
	print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
print "This took: ", y - x