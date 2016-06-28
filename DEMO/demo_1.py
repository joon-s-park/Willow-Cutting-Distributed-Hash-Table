import sys
sys.path.insert(0, '../')

from PDBST import *




ht = PDBST(0, 20)

for i in range(20):
    ht.put(i, i)

print ""
print "*********************************************************************"
print "************* DEMO 1: 20 Puts in PDBST of Different Range ***********"
print "*********************************************************************"
print ""
print ""
print "[PDBST 1]"
print "    1) Range: 0 ~ 20"
print "    2) Operation Done: for i in range(20): pdbst.put(i,i)"
print ""
print ht


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

ht = PDBST(0, 1000)

for i in range(20):
    ht.put(i, i)

print ""
print ""
print "[PDBST 2]"
print "    1) Range: 0 ~ 1000"
print "    2) Operation Done: for i in range(20): pdbst.put(i,i)"
print ""
print ht

