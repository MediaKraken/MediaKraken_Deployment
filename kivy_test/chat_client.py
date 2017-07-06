from twisted.internet import reactor, stdio, protocol
from twisted.protocols import basic
from twisted.internet import ssl

class Echo(basic.LineReceiver):
    def connectionMade(self):
        print "Welcome to the Chat, you have now connected"

        # send some text when we connect
        self.sendLine('hello')

    def lineReceived(self, line):
        print 'client received:', line

        if len(line) > 10:
            self.sendLine('exit')
        else:
            # send a response in 2 seconds
            reactor.callLater(2, self.sendLine, '>' + line)

    def connectionLost(self, reason):
        reactor.stop()


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo

factory = EchoClientFactory()
reactor.connectSSL("localhost", 7500, factory, ssl.ClientContextFactory())
reactor.run()