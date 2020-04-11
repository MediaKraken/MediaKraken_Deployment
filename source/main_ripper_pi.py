"""
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
"""

import json
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from common import common_global
from common import common_hardware_arduino_usb_serial
from common import common_logging_elasticsearch
from common import common_signal
from crochet import wait_for, setup

setup()

from kivy.lang import Builder
from twisted.internet import reactor, protocol
from twisted.protocols import basic

import kivy
from kivy.app import App

kivy.require('1.11.0')
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.config import Config

twisted_connection = None
mk_app = None
thread_status = None

# moving here before anything is setup for Kivy or it doesn't work
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    Config.set('graphics', 'multisamples', '0')
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
else:
    if os.uname()[4][:3] == 'arm':
        # find real resolution
        window_sizes = Window.size
        print('window', window_sizes, flush=True)
        # TODO this is currently set to the "official" raspberry pi touchscreen
        Config.set('graphics', 'width', 800)
        Config.set('graphics', 'height', 480)
        Config.set('graphics', 'fullscreen', 'fake')


class MKEcho(basic.LineReceiver):
    MAX_LENGTH = 32000000  # pylint: disable=C0103

    def connectionMade(self):
        global twisted_connection
        twisted_connection = self
        common_global.es_inst.com_elastic_index('info', {'stuff': "connected successfully (echo)!"})

    def lineReceived(self, line):
        global mk_app
        common_global.es_inst.com_elastic_index('info', {'linereceived len': len(line)})
        # common_global.es_inst.com_elastic_index('info', {'stuff':'linereceived: %s', line)
        # common_global.es_inst.com_elastic_index('info', {'stuff':'app: %s', mk_app)
        # TODO get the following line to run from the application thread
        MediaKrakenApp.process_message(mk_app, line)

    def connectionLost(self, reason):
        common_global.es_inst.com_elastic_index('error', {'stuff': "connection lost!"})
        # reactor.stop() # leave out so it doesn't try to stop a stopped reactor

    def sendline_data(self, line):
        common_global.es_inst.com_elastic_index('info', {'sending': line})
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

    def worker(self, spinner_one_text, spinner_two_text, spinner_three_text, spinner_four_text):
        """
        Worker thread for ripper
        """
        global thread_status
        buffer_busy = False
        buffer_spool = 'one'
        if self.arm_arduino is None:
            self.arduino_connect()
        while thread_status:
            if buffer_busy is False:
                # position for pickup disc for buffing
                if spinner_one_text is not None and spinner_one_text.find('Buff') != -1:
                    self.track_arduino.com_arduino_usb_serial_writestring(
                        'track|%s' % self.spindles_media_to_process[1]['Pos'])
                    buffer_spool = 'one'
                elif spinner_two_text is not None and spinner_two_text.find('Buff') != -1:
                    self.track_arduino.com_arduino_usb_serial_writestring(
                        'track|%s' % self.spindles_media_to_process[2]['Pos'])
                    buffer_spool = 'two'
                elif spinner_three_text is not None and spinner_three_text.find('Buff') != -1:
                    self.track_arduino.com_arduino_usb_serial_writestring(
                        'track|%s' % self.spindles_media_to_process[3]['Pos'])
                    buffer_spool = 'three'
                elif spinner_four_text is not None and spinner_four_text.find('Buff') != -1:
                    self.track_arduino.com_arduino_usb_serial_writestring(
                        'track|%s' % self.spindles_media_to_process[4]['Pos'])
                    buffer_spool = 'four'
                self.pickup_cd(buffer_spool)
                self.load_buffer()
                buffer_busy = True
                self.buff_cd()
                self.unload_buffer()
                buffer_busy = False
            # find/load next disc to rip
            self.next_disc(1, spinner_one_text)
            self.next_disc(2, spinner_two_text)
            self.next_disc(3, spinner_three_text)
            self.next_disc(4, spinner_four_text)
            if thread_status is False:
                break
            time.sleep(1)

    def next_disc(self, spinner_no, spinner_text):
        for drive_status in self.rom_drives:
            if drive_status['Status'] is None and (drive_status['Type'] == spinner_text
                                                   or (drive_status['Type'] == 'DVD'
                                                       and spinner_text == 'Audio CD')):
                # load this one
                self.track_arduino.com_arduino_usb_serial_writestring(
                    'track|%s' % self.spindles_media_to_process[spinner_no]['Pos'])
                self.pickup_cd()
                self.load_drive(drive_status)
                # crochet message since thread to have main pc eject proper drive
                # which then starts the rip process
                self.send_twisted_message_thread(json.dumps({'Type': 'Rip',
                                                             'Target': drive_status['Device']}))

    def pickup_cd(self):
        # lower arm till cd contact or find empty
        self.arm_arduino.com_arduino_usb_serial_writestring('pickup')
        # TODO if hit limiter......None the spinner

    def load_buffer(self):
        # move track to buffer
        self.track_arduino.com_arduino_usb_serial_writestring(
            'track|%s' % self.buffer_drives[1]['Pos']['Track'])
        # drop disc
        self.arm_arduino.com_arduino_usb_serial_writestring(
            'drop|%s' % self.buffer_drives[1]['Pos']['Arm'])

    def load_drive(self, drive_status):
        # move to track position for drive
        self.track_arduino.com_arduino_usb_serial_writestring(
            'track|%s' % drive_status['Pos']['Track'])
        # drop disc
        self.arm_arduino.com_arduino_usb_serial_writestring(
            'drop|%s' % drive_status['Pos']['Arm'])

    def arduino_connect(self):
        # connect to arduinos and reset arm/track
        self.arm_arduino = common_hardware_arduino_usb_serial.CommonHardwareArduino(
            baud_rate='1200')
        self.track_arduino = common_hardware_arduino_usb_serial.CommonHardwareArduino(
            baud_rate='1200')

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
        content = MediaKrakenNotificationScreen(
            ok_button=self.dismiss_notification_popup)
        content.ids.message_text.text = message
        self._notification_popup = Popup(
            title=header, content=content, size_hint=(0.9, 0.9))
        self._notification_popup.open()

    def build(self):
        global mk_app
        mk_app = self
        root = MediaKraken()
        self.config = self.load_config()
        self.settings_cls = SettingsWithSidebar
        # turn off the kivy panel settings
        self.use_kivy_settings = False
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.connect_to_server()
        self.arm_arduino = None
        self.track_arduino = None
        self.spindles_media_to_process = [{1: {'Pos': 0, 'Empty': True},
                                           2: {'Pos': 200, 'Empty': True},
                                           3: {'Pos': 400, 'Empty': True},
                                           4: {'Pos': 600, 'Empty': True}}]
        self.spindles_media_processed = [{1: {'Pos': 1000, 'Discs': 0},
                                          2: {'Pos': 1200, 'Discs': 0},
                                          3: {'Pos': 1300, 'Discs': 0},
                                          4: {'Pos': 1400, 'Discs': 0}}]
        self.spindles_error = [{1: {'Pos': 1500, 'Discs': 0}}]
        self.buffer_drives = [{1: {'Pos': {'Track': 1, 'Arm': 2}}}]
        self.rom_drives = [
            {1: {'Type': 'DVD', 'Pos': {'Track': 1, 'Arm': 2}}, 'Status': None, 'Spindle': None,
             'Device': None},
            {2: {'Type': 'DVD', 'Pos': {'Track': 1, 'Arm': 2}, 'Status': None, 'Spindle': None,
                 'Device': None}},
            {3: {'Type': 'DVD', 'Pos': {'Track': 1, 'Arm': 2}, 'Status': None, 'Spindle': None,
                 'Device': None}},
            {4: {'Type': 'BluRay', 'Pos': {'Track': 1, 'Arm': 2}, 'Status': None, 'Spindle': None,
                 'Device': None}},
            {5: {'Type': 'HDDVD', 'Pos': {'Track': 1, 'Arm': 2}}, 'Status': None, 'Spindle': None,
             'Device': None},
            {5: {'Type': 'UHD', 'Pos': {'Track': 1, 'Arm': 2}}, 'Status': None, 'Spindle': None,
             'Device': None}]
        return root

    @wait_for(timeout=5.0)
    def connect_to_server(self):
        common_global.es_inst.com_elastic_index('info', {'stuff': 'conn server'})
        if self.config is not None:
            common_global.es_inst.com_elastic_index('info', {'stuff': 'here in connect to server'})
            reactor.connectTCP('10.1.0.1', 7000, MKFactory())

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
        common_global.es_inst.com_elastic_index('info', {"Got Message": server_msg})
        common_global.es_inst.com_elastic_index('info', {"len total": len(server_msg)})
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident',
                                                         'UUID': str(uuid.uuid4())}))
        else:
            common_global.es_inst.com_elastic_index('error', {'stuff': "unknown message type"})

    def main_mediakraken_event_button_start(self, *args):
        global thread_status
        common_global.es_inst.com_elastic_index('info', {"start select": args})
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.worker, self.root.ids.spinner_one.text,
                                     self.root.ids.spinner_two.text,
                                     self.root.ids.spinner_three.text,
                                     self.root.ids.spinner_four.text)
            common_global.es_inst.com_elastic_index('info', {'stuff': future.result()})
        thread_status = True

    def main_mediakraken_event_button_stop(self, *args):
        global thread_status
        common_global.es_inst.com_elastic_index('info', {"stop select": args})
        thread_status = False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        common_global.es_inst.com_elastic_index('info', {"keycode received": keycode})
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
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('ripper_pi',
                                                                             debug_override='sys')
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # load the kivy's here so all the classes have been defined
    Builder.load_file('ripper/kivy_layouts/main.kv')
    Builder.load_file('ripper/kivy_layouts/KV_Layout_Notification.kv')
    # adding this since windows10 can run on PI now
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        pass  # as os.uname doesn't exist in windows
    else:
        # so the raspberry pi doesn't crash
        if os.uname()[4][:3] != 'arm':
            Window.fullscreen = 'auto'
    MediaKrakenApp().run()
