from __future__ import absolute_import, division, print_function, unicode_literals
from kivy.support import install_twisted_reactor
install_twisted_reactor()
import kivy
kivy.require('1.10.0')
from kivy.app import App
from twisted.internet import reactor, protocol
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
        if len(line) > 10:
            self.sendLine('exit'.encode("utf8"))
        else:
            # send a response in 2 seconds
            reactor.callLater(2, self.sendLine, ('>' + line).encode("utf8"))

    def connectionLost(self, reason):
        reactor.stop()


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo


class MediaKrakenApp(App):

    def build(self):
        root = MediaKrakenApp()
        self.connect_to_server()
        return root

    def connect_to_server(self):
        print('conn server')
        reactor.connectSSL('localhost', 7500,
                           EchoClientFactory(), ssl.ClientContextFactory())
        #reactor.run()

    def process_message(self, server_msg):
        print("len: %s", len(server_msg))

if __name__ == '__main__':
    MediaKrakenApp().build()
