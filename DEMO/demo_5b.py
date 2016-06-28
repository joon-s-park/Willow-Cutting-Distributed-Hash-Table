import sys
sys.path.insert(0, "/home/jcarste1/cs87/labs/final/")

from WCDHTclient import *
import threading
from datetime import datetime

for i in range(500):
	num_connected = 0
	print "access ",i
	close = 0
	if i == 499:
		close=0
	accessServer('localhost', utils.GET, i, close=close, num_connected=num_connected)

start = datetime.now()
reactor.run()
end = datetime.now()

print "1000 Puts took ",end-start,"seconds."