from BST import BST
from linkedList import LinkedList as LL
from time import time
from willowCuttingHashTable import WillowCuttingHashTable
from chainedHashTable import ChainedHashTable

import sys, random


def main():

	sys.setrecursionlimit(10000)

	if len(sys.argv) != 4:
		print "Invalid Syntax\nUsage: performanceTest.py filename chainedLoad willowLoad\n"
		sys.exit(1)

	filename = sys.argv[1]
	chainedLoad = sys.argv[2]
	willowLoad = sys.argv[3]

	f = open(filename, "r")
	data = f.read().split()
	f.close()
	
	size = len(data)

	print "Using %d words" % size

	chained = ChainedHashTable(12, chainedLoad, BST)
	willow = WillowCuttingHashTable(willowLoad, 0, size)

    #shuffling the keys for later
	shuffledKeys = range(size)
	random.shuffle(shuffledKeys)

	print "Timing put"

	start = time()


	for i in range(size):
		#print "putting bucket ",i
		# print i
		chained[i] = data[i]

	chainedPutTime = time() - start

	start = time()
	for i in range(size):
		willow[i] = data[i]

	willowPutTime = time() - start

	# for i in range(size):
	# 	print willow[i],
	print "Willow time: %f Chained time: %f" % (willowPutTime, chainedPutTime)

	print "Timing get (random)"

	start = time()


	for i in shuffledKeys:
		#print "putting bucket ",i
		x = chained[i]
		# print x

	chainedPutTime = time() - start

	start = time()
	for i in shuffledKeys:
		x = chained[i]
		# print x

	willowPutTime = time() - start

	print "Willow time: %f Chained time: %f" % (willowPutTime, chainedPutTime)

	print "Timing get (in order)"

	start = time()

	for i in range(size):
		#print "putting bucket ",i
		x = chained[i]

	chainedPutTime = time() - start

	start = time()
	for i in range(size):
		x = chained[i]

	willowPutTime = time() - start

	print "Willow time: %f Chained time: %f" % (willowPutTime, chainedPutTime)




main()