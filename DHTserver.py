from twisted.internet import reactor, protocol
from twisted.protocols import basic
from chainedHashTable import ChainedHashTable
import struct, sys, utils, linkedList, BST

class DHTProtocol(protocol.Protocol):

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self,data):
        print "received data"
        print "> Received: ``%s''" % data
         
        recv_type, messageID, key = struct.unpack("!BBI", data[:6])
        if(recv_type == utils.PUT):
            send_type = utils.REPLY_PUT
            value = data[6:]
            self.factory.put(key, value)

            send_string = struct.pack("!BBI", send_type, messageID, key)

        elif(recv_type == utils.GET):
            send_type = utils.REPLY_GET
            ret = self.factory.get(key)
            if not ret:
                send_type = utils.ERROR
                ret = "Could not find the key: "+str(key)
            send_string = struct.pack("!BBI",send_type, messageID, key) + ret
        
        elif(recv_type == utils.DELETE):
            ret = ""
            send_type = utils.REPLY_DELETE
            try:
                self.factory.delete(key)
            except KeyError:
                send_type = utils.ERROR
                ret = "Could not find the key: "+str(key)
            send_string = struct.pack("!BBI",send_type, messageID, key) + ret

        self.transport.write(send_string)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

class DHTFactory(protocol.ServerFactory):
    protocol = DHTProtocol

    def __init__(self, capacity, load, dataStructure):
        self.capacity = capacity
        self.load = load
        self.dataStructure = dataStructure
        self.numConnections = 0
        self.hashTable = ChainedHashTable(capacity, load, dataStructure)

    def put(self, key, value):
        return self.hashTable.put(key, value)

    def get(self, key):
        return self.hashTable.get(key)

    def delete(self, key):
        return self.hashTable.delete(key)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: DHTserver.py initialCapacity loadFactor {LL|BST}"
        sys.exit(1)

    if sys.argv[3] == "LL":
        dataStructure = linkedList.LinkedList
    elif sys.argv[3] == "BST":
        dataStructure = BST.BST

    else:
        print "Incorrect Datastructure"
        print "Usage: DHTserver.py initialCapacity loadFactor {LL|BST}"
        sys.exit(1)

    reactor.listenTCP(1234, DHTFactory(int(sys.argv[1]), float(sys.argv[2]), dataStructure))
    reactor.run()

