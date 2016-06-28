import sys
sys.path.insert(0, '../')

from chainedHashTable import *
from willowCuttingHashTable import *

import time


var = raw_input("Please press any key to go on: ")



ht = ChainedHashTable(12,10)



k = datetime.now() - datetime.now()
print k
x = datetime.now()
for i in range(250000):
    kx = ht.put(i,i)
    if kx != 0:
        k += kx
    # print i, " is PUT"
y = datetime.now()

print ""
print "Now, 250000 elements are in the table."
print "This took: ", y - x
print "EXPAND TIME ALONE: ",k

# print "???"


# ht = WillowCuttingHashTable(10, 0, 1000001)



# k = datetime.now() - datetime.now()
# print k

# x = datetime.now()
# for i in range(250000):
# 	kx = ht.put(i,i)
# 	if kx != 0:
# 		# print kx
# 		k += kx
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print ""
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x
# print "EXPAND TIME ALONE: ",k
