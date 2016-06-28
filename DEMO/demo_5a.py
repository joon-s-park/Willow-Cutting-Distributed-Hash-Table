import sys
sys.path.insert(0, "/home/jcarste1/cs87/labs/final/")

from WCDHTclient import *
import threading
from datetime import *

def runReactor():
	reactor.run(installSignalHandlers=0)

#reactor_thread = threading.Thread(target=runReactor)
#reactor_thread.start()

class PutProtocol(basic.Int32StringReceiver):
	messageID = random.randint(0,255)

	def connectionMade(self):
		self.factory.num_connections += 1

		self.request_type = utils.PUT
		self.key = self.factory.counter
		self.value = str(self.factory.counter)
		
		self.factory.counter += 1
		
		send_string = struct.pack("!BBI",self.request_type, self.messageID, self.key) + self.value
		self.sendString(send_string)

	def stringReceived(self, data):

		print "Received server reply..."

		recv_type, ret_messageID = struct.unpack("!BB", data[:2])        

		if ret_messageID != self.messageID:
			print "Received bad messageID"
			reactor.stop()

		if recv_type == utils.ERROR:
			value = data[6:]
			print "Error returned: ",value
		elif recv_type == utils.REPLY_GET:
			recv_type, ret_messageID, key = struct.unpack("!BBI", data[:6])
			value = data[6:]
			print "Key: ",key,"\nValue: ",value
		elif recv_type == utils.SEND_RT:
			rt = pickle.loads(data[2:])
			print "Server has routing tzable: ",rt
		elif recv_type == utils.FORWARD_REQUEST:
			mapped_ip = data[2:]

			print "Need to forward the request to: ",mapped_ip
			factory = ClientFactory(self.request_type, self.key, self.value)
			reactor.connectTCP(mapped_ip, 1234, factory)
		elif recv_type == utils.REPLY_PUT or recv_type == utils.REPLY_DELETE:
			print "Request went through"
		else:
			print "Did not receive expected recv_type, ",recv_type

		if recv_type != utils.FORWARD_REQUEST:
			#reactor.callLater(2, reactor.stop)
			pass

		self.transport.loseConnection()

class wrapperFactory(protocol.ClientFactory):
	protocol=PutProtocol

	def __init__(self):
		self.num_connections = 0
		self.counter = 0

	def clientConnectionLost(self, connector, reason):
		self.num_connections -= 1
		if self.num_connections == 0:
			reactor.stop()

index = 0
index_str = "0"

factory = wrapperFactory()

for i in range(500):
	print "access ",i
	reactor.connectTCP('localhost', 1234, factory)

start = datetime.now()
reactor.run()
end = datetime.now()

print "1000 Puts took ",end-start,"seconds."
