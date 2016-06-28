from twisted.internet import reactor, protocol
import random, sys, struct, utils

class ClientProtocol(protocol.Protocol):
    messageID = random.randint(0,255)
    
    def connectionMade(self):
        request_type = self.factory.request_type
        key = self.factory.key
        send_string = struct.pack("!BBI",request_type, self.messageID, key)
        if(self.factory.request_type == utils.PUT):
            send_string += self.factory.value

        self.transport.write(send_string)

    def dataReceived(self, data):

        print "Received server reply..."

        recv_type, ret_messageID, key = struct.unpack("!BBI", data[:6])        
        value = data[6:]

        if ret_messageID != self.messageID:
            print "Received bad messageID"
            sys.exit(1)

        if recv_type == utils.ERROR:
            print "Error returned: ",value
        elif recv_type == utils.REPLY_GET:
            print "Key: ",key,"\nValue: ",value
        else:
            print "Request successfully completed"

        self.transport.loseConnection()


class ClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol

    def __init__(self, request_type, key, value=None):
        self.request_type = request_type
        self.key = key
        self.value = value

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'Connection lost: ', reason.getErrorMessage()
        reactor.stop()

def accessServer(request_type, key, value=None):
    reactor.connectTCP('localhost', 1234, ClientFactory(request_type, key, value))
    reactor.run()

if __name__ == "__main__":

    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print "Usage DHTclient.py request_type key [value]"
        sys.exit(1)

    rt_input = sys.argv[1]
    request_type = 0
    if rt_input == "PUT" or rt_input == "put":
        request_type = utils.PUT
    elif rt_input == "GET" or rt_input == "get":
        request_type = utils.GET
    elif rt_input == "DELETE" or rt_input == "delete":
        request_type = utils.DELETE
    else:
        print "Error: request types can only be put, get or delete"
        print "Usage: DHTclient.py request_type key [value]"
        sys.exit(1)

    if len(sys.argv) == 3:
        accessServer(request_type, int(sys.argv[2]))
    else:
        accessServer(request_type, int(sys.argv[2]), sys.argv[3])

