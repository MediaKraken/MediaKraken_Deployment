from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import absolute_import, division, print_function, unicode_literals
# install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
from kivy.lang import Builder
install_twisted_reactor()
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import ssl
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image, AsyncImage
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, \
    StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.settings import SettingsWithSidebar
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.lang import Builder
from kivy.base import EventLoop
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.graphics.instructions import Canvas
from kivy.graphics import Color, Rectangle
from kivy.cache import Cache
from kivy.animation import Animation
from kivy.metrics import sp
from kivy.graphics import *
from kivy.graphics.texture import Texture
from functools import partial
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

# factory = EchoClientFactory()
# reactor.connectSSL("localhost", 7500, factory, ssl.ClientContextFactory())
# reactor.run()

class MediaKrakenApp(App):
    connection = None

    def exit_program(self):
        pass

    def dismiss_popup(self):
        self._popup.dismiss()

    def build(self):
        global metaapp
        root = MediaKrakenApp()
        # turn off the kivy panel settings
        self.use_kivy_settings = False
        metaapp = self
        self.connect_to_server()
        return root

    def connect_to_server(self):
        print('conn server')
        reactor.connectSSL('localhost', 7500,
                           EchoClientFactory(self), ssl.ClientContextFactory())
        #reactor.run()

    def process_message(self, server_msg):
        print("len: %s", len(server_msg))
        proxy_image_demo = Loader.image(server_msg)
        proxy_image_demo.bind(on_load=self._image_loaded_home_demo)

    def _image_loaded_home_demo(self, proxyImage):
        if proxyImage.image.texture:
            self.root.ids.main_home_demo_image.texture = proxyImage.image.texture

if __name__ == '__main__':
    Builder.load_file('kivy_layouts/main.kv')
    MediaKrakenApp().build()
