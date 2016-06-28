

class RoutingTable:

	def __init__(self):
		self.table = {}

	def addNode(self, ip, lowerBound, upperBound):
		self.table[ip] = (lowerBound, upperBound)

	def getNode(self, num):
		for ip,(l,u) in self.table.iteritems():
			if num >= l and num <= u:
				return ip

	def __str__(self):
		string = ""
		for ip,(l,u) in self.table.iteritems():
			string += str(ip) + ": (" + str(l) + ", " + str(u) +")\n"

		return string

	def getAllIP(self):
		return self.table.keys()

	def updateRange(self, ip, lowerBound, upperBound):
		self.table[ip] = (lowerBound, upperBound)