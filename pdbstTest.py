# This program is designed to test our PDBST implementation
from PDBST import *
from BST import *
import sys, math, random

def main():

	if len(sys.argv) != 2:
		print "Invalid Syntax\nUsage: pdbstTest.py filename\n"

	filename = sys.argv[1]

	f = open(filename, "r")
	data = f.read().split()
	f.close()
	
	size = len(data)

	print "Adding %s words to the data structure\n" % size

	pdbst = PDBST(0, size)
	#pdbst = BST()

	for i,w in enumerate(data):
		pdbst[i] = w

	print pdbst

	print "\nGetting each bucket in order:\n"

	for i in range(size):
		print pdbst[i],

	print "\n\nDeleting half of the tree:\n"

	deletedList = []
	for i in range(size/2):
		x = random.randint(0, len(data)-1)
		while(x in deletedList):
			x = random.randint(0, len(data)-1)
		#print "deleting: ",x
		deletedList.append(x)
		pdbst.delete(x)

	print "\n\n",pdbst



main()