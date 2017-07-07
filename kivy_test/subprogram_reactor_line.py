from __future__ import absolute_import, division, print_function, unicode_literals
import base64
import json
from twisted.internet import reactor, protocol, stdio
from twisted.protocols import basic
from twisted.internet import ssl

lines_received = 0

class Echo(basic.LineReceiver):
    print("Welcome to Chat")
    MAX_LENGTH = 32000000  # pylint: disable=C0103

    def connectionMade(self):
        print("A new client has connected")

    def lineReceived(self, line):
        global lines_received
        lines_received += 1
        print('server received:', line)
        print('server received bytes:', len(line))
        if lines_received == 2:
            f = open("test.jpg", "w")  # opens file with name of "test.txt"
            f.write(base64.b64decode(json.loads(line)['Image']))
            f.close()
        #print('server sent:', line, '\n')
        self.sendLine(line.encode("utf8"))
        if line=="exit":
             self.transport.loseConnection()


class EchoServerFactory(protocol.ServerFactory):
   protocol = Echo


reactor.listenSSL(7500, EchoServerFactory(), ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
reactor.run()

