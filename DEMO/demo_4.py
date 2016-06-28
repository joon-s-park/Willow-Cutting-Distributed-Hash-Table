import sys
sys.path.insert(0, '../')

from willowCuttingHashTable import *
import time



print ""
print "*********************************************************************"
print "* DEMO 4: 25,000 Puts in willowCuttingHT with different loadFactor**"
print "*********************************************************************"
print ""
print " LoadFactor 1) 1"
print " LoadFactor 2) 10"
print " LoadFactor 3) 100"
print " LoadFactor 4) 1000"
print ""

var = raw_input("Please press any key to go on: ")

# print ""
# print "[curr willowCuttingHashTable]"
# print "    1) loadFactor: 0.8"
# print "    2) chained data structure: PDBST"
# print "    3) range: 0 to 10000001"
# print "    4) Operation Done: for i in range(50000): ht.put(i,i)"
# print ""
# print ""

ht = WillowCuttingHashTable(1, 0, 10000001)

x = datetime.now()
for i in range(25000):
	ht.put(i, i)
	print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
z1 = y - x
print "This took: ", z1
time.sleep(1)

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

ht = WillowCuttingHashTable(10, 0, 10000001)

x = datetime.now()
for i in range(25000):
	ht.put(i, i)
	print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
z2 = y - x
print "This took: ", z2
time.sleep(1)

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

ht = WillowCuttingHashTable(100, 0, 10000001)

x = datetime.now()
for i in range(25000):
	ht.put(i, i)
	print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
z3 = y - x
print "This took: ", z3
time.sleep(1)

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

ht = WillowCuttingHashTable(1000, 0, 10000001)

x = datetime.now()
for i in range(25000):
	ht.put(i, i)
	print i, " is PUT"
y = datetime.now()

print ""
print "Now, 200000 elements are in the table."
z4 = y - x
print "This took: ", z4
time.sleep(1)

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

print ""
print ""
print " LoadFactor 1) 1    took: ", z1
print " LoadFactor 2) 10   took: ", z2
print " LoadFactor 3) 100  took: ", z3
print " LoadFactor 4) 1000 took: ", z4
print ""