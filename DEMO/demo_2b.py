import sys
sys.path.insert(0, '../')

from PDBST import *
import time




print ""
print "*********************************************************************"
print "**************** DEMO 2 (Part b.): 1000 Puts in PDBST ***************"
print "*********************************************************************"
print ""
print "[PDBST]"
print "    1) Range: 0 ~ 1001"
print "    2) Operation Done: for i in range(1000): pdbst.put(i,i)"
print ""
print ""
var = raw_input("Please press any key to go on: ")





ht = PDBST(0, 1001)

for i in range(1000):
    ht.put(i, i)
    print "%d is put." % i

print ht


