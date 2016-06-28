from twisted.internet import reactor, protocol
from twisted.protocols import basic
from willowCuttingHashTable import WillowCuttingHashTable
import struct, sys, utils, linkedList, BST, random, time, threading
import cPickle as pickle
from routingTable import RoutingTable
from commands import getoutput as run
from WCDHTclient import *

possible_types = ['PUT', 'GET', 'DELETE', 'REPLY_PUT', 'REPLY_GET','REPLY_DELETE','ERROR','JOIN_REQUEST','RANGE_SUGGESTION','RANGE_ACCEPT','SEND_CHUNK','REQUEST_RT','SEND_RT','RT_ACK','FORWARD_REQUEST']
type_map = {}
for i in range(1,16):
    type_map[i] = possible_types[i-1]

class WCDHTProtocol(basic.Int32StringReceiver):

    def connectionMade(self):
        print "incoming connection from: ",self.transport.getPeer().host
        self.factory.numConnections += 1

    def stringReceived(self,data):
         
        recv_type = ord(data[0])

        if(recv_type == utils.PUT):
            print "Received type: PUT"
            recv_type, messageID, key = struct.unpack("!BBI", data[:6])
            send_type = utils.REPLY_PUT
            value = data[6:]
            print "Key: %d Value: %s" % (key, value)

            hash_key = self.factory.hash(key)
            mapped_ip = self.factory.routingTable.getNode(hash_key)
            print "Hashed key: ",hash_key," mapped_ip: ",mapped_ip," is self? ",(mapped_ip == self.factory.ip)
            if mapped_ip == self.factory.ip:
                try:
                    ret = ""
                    self.factory.put(key, value)
                except ValueError:
                    send_type = utils.ERROR
                    ret = "Key must be within values %d to %d" % (self.globalRange[0], self.globalRange[1])
                
                send_string = struct.pack("!BBI", send_type, messageID, key) + ret
            else:
                send_string = self.forwardRequest(mapped_ip, messageID)

        elif(recv_type == utils.GET):
            print "Received type: GET"
            recv_type, messageID, key = struct.unpack("!BBI", data[:6])
            print "Key: ",key
            mapped_ip = self.factory.routingTable.getNode(self.factory.hash(key))
            print "mapped ip to: ",mapped_ip
            if mapped_ip == self.factory.ip:
                print "That is me!"
                try:
                    ret = self.factory.get(key)
                    if not ret:
                        send_type = utils.ERROR
                        ret = "Could not find the key: "+str(key)
                    send_type = utils.REPLY_GET
                except ValueError:
                    send_type = utils.ERROR
                    ret = "Key must be within values %d to %d" % (self.globalRange[0], self.globalRange[1])
                    
                send_string = struct.pack("!BBI",send_type, messageID, key) + ret
            else:
                "Forwarding..."
                send_string = self.forwardRequest(mapped_ip, messageID)

        elif(recv_type == utils.DELETE):
            print "Received type: DELETE"
            recv_type, messageID, key = struct.unpack("!BBI", data[:6])
            print "Key: ",key
            ret = ""
            send_type = utils.REPLY_DELETE
            mapped_ip = self.factory.routingTable.getNode(self.factory.hash(key))
            if mapped_ip == self.factory.ip:
                try:
                    self.factory.delete(key)
                except KeyError:
                    send_type = utils.ERROR
                    ret = "Could not find the key: "+str(key)
                except ValueError:
                    send_type = utils.ERROR
                    ret = "Key must be within values %d to %d" % (self.globalRange[0], self.globalRange[1])

                send_string = struct.pack("!BBI",send_type, messageID, key) + ret
            else:
                send_string = self.forwardRequest(mapped_ip, messageID)


        elif(recv_type == utils.JOIN_REQUEST):
            print "Received type: JOIN_REQUEST"
            messageID = ord(data[1])

            capacity = self.factory.hashTable.capacity

            if capacity <= 4:
                send_type = utils.ERROR
                ret = "Not enough data to split"
                send_string = struct.pack("!BB",send_type, messageID) + ret
            else:
                num_pdbst = self.factory.hashTable.capacity/4
                send_type = utils.RANGE_SUGGESTION
                ht_upperBound = self.factory.hashTable.upperBound
                ht_lowerBound = self.factory.hashTable.buckets[-1*num_pdbst].lowerBound
                ht_range = ht_upperBound - ht_lowerBound

                send_string = struct.pack("!BBI", send_type, messageID, ht_range)

        elif(recv_type == utils.RANGE_ACCEPT):
            print "Received type: RANGE_ACCEPT"
            messageID = ord(data[1])

            capacity = self.factory.hashTable.capacity
            print "Capacity of ht: ",capacity
            num_pdbst = capacity/4
            split_index = capacity - num_pdbst
            #split_index = capacity - capacity/10
            new_ht, send_ht = self.factory.hashTable.splitTable(split_index)
            self.factory.hashTable = new_ht

            host_ip = self.transport.getPeer().host

            self.factory.routingTable.addNode(host_ip, send_ht.lowerBound, send_ht.upperBound)
            self.factory.routingTable.updateRange(self.factory.ip, self.factory.hashTable.lowerBound, self.factory.hashTable.upperBound)

            print "New routing table:\n",self.factory.routingTable

            for ip in self.factory.routingTable.getAllIP():    
                if ip != self.factory.ip and ip != host_ip:
                    b_factory = protocol.ClientFactory()
                    b_factory.protocol = BroadcastProtocol
                    b_factory.routingTable = self.factory.routingTable
                    print "Broadcasting to: ",ip
                    reactor.connectTCP(ip, 1234, b_factory)


            send_type = utils.SEND_CHUNK
            send_string = struct.pack("!BBII", send_type, messageID, self.factory.globalRange[0], self.factory.globalRange[1])
            send_string += pickle.dumps(send_ht, -1)

        elif(recv_type == utils.REQUEST_RT):
            print "Received type: REQUEST_RT"
            messageID = ord(data[1])
            send_type = utils.SEND_RT
            send_string = struct.pack("!BB", send_type, messageID)
            send_string += pickle.dumps(self.factory.routingTable)

        elif recv_type == utils.SEND_RT:
            print "Received type: SEND_RT"
            messageID = ord(data[1])

            new_routingTable = pickle.loads(data[2:])
            self.factory.routingTable = new_routingTable
            print "New routing table:\n",new_routingTable

            send_type = utils.RT_ACK
            send_string = struct.pack("!BB", send_type, messageID)


        print "Sending string type: ",type_map[ord(send_string[0])]
        #print "String: ", send_string
        print "String size: ",len(send_string),"\n"
        self.sendString(send_string)

    def connectionLost(self, reason):
        #print "Connection Lost: ",reason.getErrorMessage(), "\n"
        self.factory.numConnections -= 1

    def lengthLimitExceeded(self,length):
            print "length limit exceeded, length: ",length

    def forwardRequest(self, mapped_ip, messageID):
        send_type = utils.FORWARD_REQUEST
        return struct.pack("!BB", send_type, messageID) + mapped_ip


class WCDHTFactory(protocol.ServerFactory):
    protocol = WCDHTProtocol

    def __init__(self, load, ip=None):
        print "SERVER STARTING"
        self.numConnections = 0
        self.routingTable = None
        self.hashTable = None
        self.ip = run("ifconfig | awk '/inet addr/{print substr($2,6)}'").splitlines()[0]
        self.globalRange = None

        if ip:
            # tables = []
            # factory=WillowJoinFactory(tables)
            # reactor.connectTCP(ip, 1234, factory)
            # reactor.listenTCP(1234, self)
            # reactor.run()

            # while len(tables) != 2:
            #     pass
            # print "got tables!!"
            # # hashTable = tables[0]
            # # routingTable = tables[1]
            # print self.hashTable
            # print self.routingTable
            pass
        else:
            self.hashTable = WillowCuttingHashTable(load, 0, 5000)
            self.routingTable = RoutingTable()
            #get current ip address
            self.routingTable.addNode(self.ip, 0, 5000)
            self.globalRange = (self.hashTable.lowerBound, self.hashTable.upperBound)



    def put(self, key, value):
        return self.hashTable.put(key, value)

    def get(self, key):
        return self.hashTable.get(key)

    def delete(self, key):
        return self.hashTable.delete(key)

    def hash(self, key):
        return self.hashTable._unboundedHash(key)


class BroadcastProtocol(basic.Int32StringReceiver):
    messageID = random.randint(0,255)

    def connectionMade(self):
        send_type = utils.SEND_RT
        send_string = struct.pack("!BB", send_type, self.messageID)
        send_string += pickle.dumps(self.factory.routingTable)

        print "Send type: SEND_RT"
        self.sendString(send_string)

    def stringReceived(self, data):
        recv_type, messageID = struct.unpack("!BB", data)

        if messageID != self.messageID:
            print "Bad message id for rt_ack"

        if recv_type != utils.RT_ACK:
            print "Client: %s did not get the updated routing table" % self.transport.getPeer().host
        else:
            print "Client: %s got the updated routing table!" % self.transport.getPeer().host
        self.transport.loseConnection()





class WillowJoin(basic.Int32StringReceiver):
    messageID = random.randint(0,255)
    
    def connectionMade(self):
        request_type = utils.JOIN_REQUEST
        send_string = struct.pack("!BB", request_type, self.messageID)

        self.sendString(send_string)

    def stringReceived(self, data):
        recv_type, ret_messageID = struct.unpack("!BB", data[0:2])

        if ret_messageID != self.messageID:
            print "Received out of order messageID....."
            sys.exit(1)
        
        if recv_type == utils.RANGE_SUGGESTION:
            print "Received type: RANGE_SUGGESTION"
            recv_type, ret_messageID, suggested_range = struct.unpack("!BBI", data)
            while(True):
                answer = raw_input("Accept range of %d? [0/1]" % suggested_range)
                if answer != "1" and answer != "0":
                    continue
                else:
                    break

            if int(answer) == 1:
                send_type = utils.RANGE_ACCEPT
                self.messageID = random.randint(0,255)
                send_string = struct.pack("!BB", send_type, self.messageID)
                self.sendString(send_string)
            else:
                print "Now exiting..."
                sys.exit(1)

        elif recv_type == utils.SEND_CHUNK:
            print "Received type: SEND_CHUNK"
            recv_type, ret_messageID, global_lower, global_upper = struct.unpack("!BBII", data[0:10])
            self.globalRange = (global_lower, global_upper)
            pickle_string = data[10:]
            self.factory.hashTable = pickle.loads(pickle_string)

            print "Got hashtable chunk:"
            #print self.factory.hashTable

            send_type = utils.REQUEST_RT
            self.messageID = random.randint(0,255)
            send_string = struct.pack("!BB", send_type, self.messageID)
            self.sendString(send_string)

        elif recv_type == utils.SEND_RT:
            print "Received type: SEND_RT"
            print "Got routing table:"
            pickle_string = data[2:]
            self.factory.routingTable = pickle.loads(pickle_string)
            print self.factory.routingTable

            self.factory.setParentValues()

            self.transport.loseConnection()

        elif recv_type == utils.ERROR:
            print "Received type: ERROR"
            print "Error received: ",data[2:]
            self.transport.loseConnection()

        def lengthLimitExceeded(self,length):
            print "length limit exceeded, length: ",length

class WillowJoinFactory(protocol.ClientFactory):
    protocol = WillowJoin
    hashTable = None
    routingTable = None
    server_factory = None
    globalRange = None

    def __init__(self, parent_tables):
        self.server_factory = parent_tables

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'Connection Lost: ', reason.getErrorMessage(), "\n"
        #reactor.stop()

    def setParentValues(self):
        self.server_factory.hashTable = self.hashTable
        self.server_factory.routingTable = self.routingTable
        self.server_factory.globalRange = self.globalRange
        reactor.listenTCP(1234, self.server_factory)

def join_func(ip,tables):
    reactor.connectTCP(ip, 1234, WillowJoinFactory(tables))
    reactor.run()

def server_func(hashTable, routingTable):
    reactor.listenTCP(1234, WCDHTFactory(hashTable, routingTable))
    reactor.run()


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print "Usage: DHTserver.py loadFactor [ip_address]"
        sys.exit(1)

    hashTable = None
    routingTable = None

    load = int(sys.argv[1])

    if len(sys.argv) == 3:
        ip = sys.argv[2]
        factory = WCDHTFactory(load, ip)
        reactor.connectTCP(ip, 1234, WillowJoinFactory(factory))
    else:
        factory = WCDHTFactory(load)
        reactor.listenTCP(1234,factory)

    #reactor.listenTCP(1234, factory)
    reactor.run()

