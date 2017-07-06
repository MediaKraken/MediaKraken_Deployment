from twisted.internet import reactor, protocol, stdio
from twisted.protocols import basic
from twisted.internet import ssl

class Echo(basic.LineReceiver):
    print "Welcome to Chat"

    def connectionMade(self):
        print "A new client has connected"

    def lineReceived(self, line):
        print 'server received:', line
        print 'server sent:', line, '\n'
        self.sendLine(line)
        if line=="exit":
             self.transport.loseConnection()

class EchoServerFactory(protocol.ServerFactory):
   protocol = Echo

factory = EchoServerFactory()
reactor.listenSSL(7500, factory, ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
#reactor.listenTCP(9999, factory)
reactor.run()

