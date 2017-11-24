'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from common import common_logging
from common import common_signal
import sys
import os
import json
from crochet import wait_for, run_in_reactor, setup
setup()

from kivy.lang import Builder
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.internet import ssl
from twisted.python import log

import kivy
from kivy.app import App
kivy.require('1.10.0')
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, \
    StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image, AsyncImage
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.filechooser import FileChooserListView
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
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *

twisted_connection = None
mk_app = None


class MKEcho(basic.LineReceiver):
    MAX_LENGTH = 32000000  # pylint: disable=C0103

    def connectionMade(self):
        global twisted_connection
        twisted_connection = self
        logging.info("connected successfully (echo)!")

    def lineReceived(self, line):
        global mk_app
        logging.info('linereceived len: %s', len(line))
        #logging.info('linereceived: %s', line)
        #logging.info('app: %s', mk_app)
        # TODO get the following line to run from the application thread
        MediaKrakenApp.process_message(mk_app, line)

    def connectionLost(self, reason):
        logging.error("connection lost!")
        #reactor.stop() # leave out so it doesn't try to stop a stopped reactor

    def sendline_data(self, line):
        logging.info('sending: %s', line)
        self.sendLine(line.encode("utf8"))

class MKFactory(protocol.ClientFactory):
    protocol = MKEcho

class MediaKraken(FloatLayout):
    """
    This is the base class that builds the gui
    """
    pass

class MediaKrakenLoginScreen(BoxLayout):
    """
    Login screen
    """
    password = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MediaKrakenNotificationScreen(BoxLayout):
    """
    Notification display
    """
    message_text = ObjectProperty(None)
    ok_button = ObjectProperty(None)

class MediaKrakenApp(App):
    global twisted_connection

    def exit_program(self):
        pass

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_notification_popup(self):
        """
        Dismiss notification popup
        """
        self._notification_popup.dismiss()

    # notification dialog
    def mediakraken_notification_popup(self, header, message):
        content = MediaKrakenNotificationScreen(ok_button=self.dismiss_notification_popup)
        content.ids.message_text.text = message
        self._notification_popup = Popup(title=header, content=content, size_hint=(0.9, 0.9))
        self._notification_popup.open()

    def build(self):
        global mk_app
        mk_app = self
        root = MediaKraken()
        self.config = self.load_config()
        self.settings_cls = SettingsWithSidebar
        # turn off the kivy panel settings
        self.use_kivy_settings = False
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.connect_to_server()
        return root

    @wait_for(timeout=5.0)
    def connect_to_server(self):
        logging.info('conn server')
        if self.config is not None:
            logging.info('here in connect to server')
            reactor.connectTCP('10.0.0.1', 5000, MKFactory())

    @wait_for(timeout=5.0)
    def send_twisted_message(self, message):
        """
        Send message via twisted reactor
        """
        MKFactory.protocol.sendline_data(twisted_connection, message)

    def send_twisted_message_thread(self, message):
        """
        Send message via twisted reactor from the crochet thread
        """
        MKFactory.protocol.sendline_data(twisted_connection, message)

    def process_message(self, server_msg):
        """
        Process network message from server
        """
        json_message = json.loads(server_msg)
        logging.info("Got Message: %s", server_msg)
        logging.info("len total: %s", len(server_msg))
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident',
                                                         'UUID': str(uuid.uuid4()),
                                                         'Platform': platform.node()}))
            # start up the image refresh since we have a connection
            Clock.schedule_interval(self.main_image_refresh, 5.0)
        else:
            logging.error("unknown message type")

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        logging.info("keycode received: %s", keycode)
        if keycode[1] == 'backspace':
            if self.root.ids._screen_manager.current == 'Main_Theater_Home':
                pass
        elif keycode[1] == 'escape':
            sys.exit()
        elif keycode[1] == 'f1':
            # display help
            pass
        return True

if __name__ == '__main__':
    # for windows exe support
    from multiprocessing import freeze_support
    freeze_support()
    # begin logging
    common_logging.com_logging_start('./log/MediaKraken_Ripper_Pi')
    log.startLogging(sys.stdout) # for twisted
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # load the kivy's here so all the classes have been defined
    Builder.load_file('ripper/kivy_layouts/main.kv')
    Builder.load_file('ripper/kivy_layouts/KV_Layout_Notification.kv')
    # so the raspberry pi doesn't crash
    if os.uname()[4][:3] != 'arm':
        Window.fullscreen = 'auto'
    MediaKrakenApp().run()
