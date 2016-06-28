from twisted.internet import reactor, protocol
from twisted.protocols import basic
import random, sys, struct, utils,time
import cPickle as pickle

class ClientProtocol(basic.Int32StringReceiver):
    messageID = random.randint(0,255)
    
    def connectionMade(self):
        request_type = self.factory.request_type
        key = self.factory.key
        send_string = struct.pack("!BBI",request_type, self.messageID, key)
        if(self.factory.request_type == utils.PUT):
            send_string += self.factory.value

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
            print "Server has routing table: ",rt
        elif recv_type == utils.FORWARD_REQUEST:
            mapped_ip = data[2:]

            print "Need to forward the request to: ",mapped_ip
            factory = ClientFactory(self.factory.request_type, self.factory.key, self.factory.value)
            reactor.connectTCP(mapped_ip, 1234, factory)
        elif recv_type == utils.REPLY_PUT or recv_type == utils.REPLY_DELETE:
            print "Request went through"
        else:
            print "Did not receive expected recv_type, ",recv_type

        if recv_type != utils.FORWARD_REQUEST:
            #reactor.callLater(2, reactor.stop)
            pass

        self.transport.loseConnection()


class ClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol

    def __init__(self, request_type, key, value=None, close=0, num_connected=None):
        self.request_type = request_type
        self.key = key
        self.value = value
        self.close = close
        self.num_connected = num_connected

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed:', reason.getErrorMessage()
        reason.printTraceback()
        #reactor.stop()

    def clientConnectionLost(self, connector, reason):
        # # print 'Connection lost: ', reason.getErrorMessage()
        # if self.num_connected:
        #     self.num_connected -= 1
        # #if self.close:
        #     #time.sleep(2)
        #     #reactor.stop()
        pass

def accessServer(ip, request_type, key, value=None, close=0, num_connected=None):
    reactor.connectTCP(ip, 1234, ClientFactory(request_type, key, value, close, num_connected))

def runReactor():
    reactor.run()

if __name__ == "__main__":

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print "Usage DHTclient.py ip request_type key [value]"
        sys.exit(1)

    ip = sys.argv[1]

    rt_input = sys.argv[2]
    request_type = 0
    if rt_input == "PUT" or rt_input == "put":
        request_type = utils.PUT
    elif rt_input == "GET" or rt_input == "get":
        request_type = utils.GET
    elif rt_input == "DELETE" or rt_input == "delete":
        request_type = utils.DELETE
    elif rt_input == "RT" or rt_input == "rt":
        request_type = utils.REQUEST_RT
    else:
        print "Error: request types can only be put, get or delete"
        print "Usage: DHTclient.py request_type key [value]"
        sys.exit(1)


    if len(sys.argv) == 4:
        accessServer(ip, request_type, int(sys.argv[3]))
        reactor.run()
    else:
        accessServer(ip, request_type, int(sys.argv[3]), sys.argv[4])
        reactor.run()

