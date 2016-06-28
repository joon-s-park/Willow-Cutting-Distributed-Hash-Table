import sys
sys.path.insert(0, '../')

from chainedHashTable import *
from willowCuttingHashTable import *

import time


var = raw_input("Please press any key to go on: ")



ht = ChainedHashTable(12,1000)

x = datetime.now()
for i in range(250000):
    ht.put(i,i)
    # print i, " is PUT"
y = datetime.now()

print "Load Factor: 1,000"
print "Now, 250000 elements are in the table."
print "This took: ", y - x




# ht = ChainedHashTable(12,5, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 5"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x




# ht = ChainedHashTable(12,10, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 10"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x


# ht = ChainedHashTable(12,20, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 20"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x


# ht = ChainedHashTable(12,50, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 50"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x


# ht = ChainedHashTable(12,100, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 100"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x

# ht = ChainedHashTable(12,500, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 500"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x

# ht = ChainedHashTable(12,1000, BST)

# x = datetime.now()
# for i in range(250000):
#     ht.put(i,i)
#     # print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 1000"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x







# ht = WillowCuttingHashTable(1000, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print ""
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x




# ht = WillowCuttingHashTable(1000, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 1000"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x



# ht = WillowCuttingHashTable(500, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 500"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x



# ht = WillowCuttingHashTable(100, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 100"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x



# ht = WillowCuttingHashTable(50, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 50"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x

# ht = WillowCuttingHashTable(20, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 20"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x

# ht = WillowCuttingHashTable(10, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 10"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x

# ht = WillowCuttingHashTable(5, 0, 1000001)

# x = datetime.now()
# for i in range(250000):
# 	ht.put(i, i)
# 	# print i, " is PUT"
# y = datetime.now()

# print "Load Factor: 5"
# print "Now, 250000 elements are in the table."
# print "This took: ", y - x