from __future__ import absolute_import, division, print_function, unicode_literals
from kivy.support import install_twisted_reactor
import base64
import json
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import ssl

class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenSSL(8000, EchoServerFactory(self), ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
        return self.label

    def handle_message(self, msg):
        #msg = msg.decode('utf-8')
        self.label.text = "received:  {}\n".format(str(len(msg)))

        f = open("test.jpg", "w")  # opens file with name of "test.txt"
        f.write(base64.b64decode(msg))
        f.close()

        if msg == "ping":
            msg = "Pong"
        if msg == "plop":
            msg = "Kivy Rocks!!!"
        #self.label.text += "responded: {}\n".format(msg)
        return msg.encode('utf-8')


if __name__ == '__main__':
    TwistedServerApp().run()
