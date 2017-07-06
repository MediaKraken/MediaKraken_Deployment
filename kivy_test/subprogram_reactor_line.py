from __future__ import absolute_import, division, print_function, unicode_literals
import base64
from twisted.internet import reactor, protocol, stdio
from twisted.protocols import basic
from twisted.internet import ssl


class Echo(basic.LineReceiver):
    print("Welcome to Chat")
    MAX_LENGTH = 32000000  # pylint: disable=C0103

    def connectionMade(self):
        print("A new client has connected")

    def lineReceived(self, line):
        print('server received:', line)
        print('server sent:', line, '\n')
        self.sendLine(line.encode("utf8"))
        if line=="exit":
             self.transport.loseConnection()


class EchoServerFactory(protocol.ServerFactory):
   protocol = Echo


factory = EchoServerFactory()
reactor.listenSSL(7500, factory, ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
reactor.run()

