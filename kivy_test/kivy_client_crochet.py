from __future__ import absolute_import, division, print_function, unicode_literals
import base64
import json
#from kivy.support import install_twisted_reactor
from crochet import wait_for, run_in_reactor, setup
setup()

#install_twisted_reactor() - will run fine frmo crochet

# A Simple Client that send messages to the Echo Server
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

        iconfile = open("poster.jpg", "rb")
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

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class TwistedClientApp(App):
    connection = None
    textbox = None
    label = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    @wait_for(timeout=5.0)
    def connect_to_server(self):
        reactor.connectSSL('localhost', 7500, EchoClientFactory(), ssl.ClientContextFactory())

    @wait_for(timeout=5.0)
    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    @wait_for(timeout=5.0)
    def send_message(self, *args):
        # msg = self.textbox.text
        # if msg and self.connection:
        #     self.connection.write(msg.encode('utf-8'))
        #     self.textbox.text = ""
        iconfile = open("poster.jpg", "rb")
        icondata = iconfile.read()
        icondata = base64.b64encode(icondata)
        self.connection.write(icondata.encode("utf8"))


    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)


if __name__ == '__main__':
    TwistedClientApp().run()
