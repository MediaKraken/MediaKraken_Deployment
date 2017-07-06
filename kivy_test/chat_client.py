from __future__ import absolute_import, division, print_function, unicode_literals
import base64
import json
from twisted.internet import reactor, stdio, protocol
from twisted.protocols import basic
from twisted.internet import ssl


class Echo(basic.LineReceiver):
    MAX_LENGTH = 32000000  # pylint: disable=C0103

    def connectionMade(self):
        print("Welcome to the Chat, you have now connected")

        # send some text when we connect
        self.sendLine('hello'.encode("utf8"))

    def lineReceived(self, line):
        print('client received:', line)

        iconfile = open("theater/images/diskette.png", "rb")
        icondata = iconfile.read()
        icondata = base64.b64encode(icondata)

        self.sendLine(json.dumps({'Image': icondata.encode("utf8")}))

        if len(line) > 10:
            self.sendLine('exit'.encode("utf8"))
        else:
            # send a response in 2 seconds
            reactor.callLater(2, self.sendLine, ('>' + line).encode("utf8"))

    def connectionLost(self, reason):
        reactor.stop()


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo

factory = EchoClientFactory()
reactor.connectSSL("localhost", 7500, factory, ssl.ClientContextFactory())
reactor.run()