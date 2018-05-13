'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

import base64
import json
import logging  # pylint: disable=W0611
import os
import platform
import subprocess
import sys
import uuid

from common import common_global
from common import common_logging_elasticsearch
from common import common_network_mediakraken
from common import common_network_mpv
from common import common_signal

logging.getLogger('twisted').setLevel(logging.ERROR)

from crochet import wait_for, setup

setup()

from kivy.lang import Builder
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.internet import ssl
from twisted.python import log

import kivy
from kivy.app import App

kivy.require('1.10.0')
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.graphics import *
from kivy.graphics.opengl import *
from kivy.graphics import *
from theater import MediaKrakenSettings

twisted_connection = None
mk_app = None


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
        self.mpv_process = None
        self.mpv_connection = None
        return root

    @wait_for(timeout=5.0)
    def connect_to_server(self):
        common_global.es_inst.com_elastic_index('info', {'stuff': 'conn server'})
        if self.config is not None:
            common_global.es_inst.com_elastic_index('info', {'stuff': 'here in connect to server'})
            if self.config.get('MediaKrakenServer', 'Host').strip() == 'None':
                # TODO if more than one server, popup list selection
                server_list = common_network_mediakraken.com_net_mediakraken_find_server()
                common_global.es_inst.com_elastic_index('info', {'server list': server_list})
                host_ip = server_list[0]
                # TODO allow pick from list and save it below
                self.config.set('MediaKrakenServer', 'Host',
                                host_ip.split(':')[0])
                self.config.set('MediaKrakenServer', 'Port',
                                host_ip.split(':')[1])
                with open(r'mediakraken.ini', 'wb') as configfile:
                    self.config.write()
            else:
                pass
            reactor.connectSSL(self.config.get('MediaKrakenServer', 'Host').strip(),
                               int(self.config.get(
                                   'MediaKrakenServer', 'Port').strip()),
                               MKFactory(), ssl.ClientContextFactory())

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
        try:
            if json_message['Type'] != "Image":
                common_global.es_inst.com_elastic_index('info', {"Got Message": server_msg})
            else:
                common_global.es_inst.com_elastic_index('info', {"Got Image Message":
                                                                     json_message['Sub'], 'uuid':
                                                                     json_message['UUID']})
        except:
            common_global.es_inst.com_elastic_index('info', {"full record": server_msg})
        common_global.es_inst.com_elastic_index('info', {"len total": len(server_msg)})
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident',
                                                         'UUID': str(uuid.uuid4()),
                                                         'Platform': platform.node()}))
            # start up the image refresh since we have a connection
            Clock.schedule_interval(self.main_image_refresh, 5.0)
        elif json_message['Type'] == "Media":
            if json_message['Sub'] == "Detail":
                self.root.ids.theater_media_video_title.text \
                    = json_message['Data']['Meta']['themoviedb']['Meta']['title']
                self.root.ids.theater_media_video_subtitle.text \
                    = json_message['Data']['Meta']['themoviedb']['Meta']['tagline']
                # self.root.ids.theater_media_video_rating = row_data[3]['']
                self.root.ids.theater_media_video_runtime.text \
                    = str(json_message['Data']['Meta']['themoviedb']['Meta']['runtime'])
                self.root.ids.theater_media_video_overview.text \
                    = json_message['Data']['Meta']['themoviedb']['Meta']['overview']
                genres_list = ''
                for ndx in range(0,
                                 len(json_message['Data']['Meta']['themoviedb']['Meta']['genres'])):
                    genres_list += (
                            json_message['Data']['Meta']['themoviedb']['Meta']['genres'][ndx][
                                'name'] + ', ')
                self.root.ids.theater_media_video_genres.text = genres_list[:-2]
                production_list = ''
                for ndx in range(0, len(json_message['Data']['Meta']['themoviedb']['Meta'][
                                            'production_companies'])):
                    production_list += (json_message['Data']['Meta']['themoviedb']['Meta'][
                                            'production_companies'][ndx]['name'] + ', ')
                self.root.ids.theater_media_video_production_companies.text = production_list[
                                                                              :-2]
        elif json_message['Type'] == 'Play':  # direct file play
            video_source_dir = json_message['Data']
            share_mapping = (
                ('/mediakraken/mnt/zfsspoo/', '/home/spoot/zfsspoo/'),)
            if share_mapping is not None:
                for mapping in share_mapping:
                    video_source_dir = video_source_dir.replace(
                        mapping[0], mapping[1])
                self.mpv_process = subprocess.Popen(['mpv', '--no-config', '--fullscreen',
                                                     '--ontop', '--no-osc', '--no-osd-bar',
                                                     '--aid=2',
                                                     '--audio-spdif=ac3,dts,dts-hd,truehd,eac3',
                                                     '--audio-device=pulse', '--hwdec=auto',
                                                     '--input-ipc-server', './mk_mpv.sock',
                                                     '%s' % video_source_dir],
                                                    shell=False)
                self.mpv_connection = common_network_mpv.CommonNetMPVSocat()
        elif json_message['Type'] == "Image":
            common_global.es_inst.com_elastic_index('info', {'stuff': "here for movie refresh"})
            if json_message['Sub2'] == "Demo":
                f = open("./image_demo", "w")
                f.write(base64.b64decode(json_message['Data']))
                f.close()
                self.demo_media_id = json_message['UUID']
                if self.first_image_demo == False:
                    common_global.es_inst.com_elastic_index('info', {'stuff': 'boom'})
                    # self.root.ids.main_home_demo_image.reload()
                    common_global.es_inst.com_elastic_index('info', {'stuff': 'boom2'})
                else:
                    common_global.es_inst.com_elastic_index('info', {'stuff': 'wha2'})
                    proxy_image_demo = Loader.image("./image_demo")
                    proxy_image_demo.bind(
                        on_load=self._image_loaded_home_demo)
                    self.first_image_demo = False
        elif json_message['Type'] == "MPV":
            self.mpv_connection.execute(json_message['Data'])
        else:
            common_global.es_inst.com_elastic_index('error', {'stuff': "unknown message type"})

    def build_config(self, config):
        """
        Build base config
        """
        config.setdefaults('MediaKrakenServer', {
            'Host': 'None',
            'Port': 8903})
        config.setdefaults('Audio', {
            'Default_Device': 'Default',
            'Channels': '7.1'})
        config.setdefaults('Passthrough', {
            'Enable': False,
            'Device': 'Default',
            'DTS': False,
            'DTSHD': False,
            'DTSX': False,
            'AC3': False,
            'EAC3': False,
            'TRUEHD': False,
            'Atmos': False})
        config.setdefaults('MediaKraken', {
            'Default_Device': 'Default'})
        config.setdefaults('Video', {
            'Blank_Displays': False,
            'Display_Screen': 'Display #1',
            'Resolution': 'Window Size',
            'Fullscreen': True,
            'Fullscreen_Window': False,
            'Sleep_Time': '3 min'})
        config.setdefaults('Library', {
            'Show_Plot_Unwatched': True,
            'Flatten_TV_Show_Seasons': 'If Only One Season',
            'Group_Movies_in_Sets': True})
        config.setdefaults('Playback', {
            'Preferred_Audio_Language': 'Original Stream Language',
            'Play_Next_Media_Automatically': False})

    def build_settings(self, settings):
        settings.add_json_panel('MediaKraken', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_base_json)
        settings.add_json_panel('Audio', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_audio_json)
        settings.add_json_panel('Video', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_video_json)
        settings.add_json_panel('Library', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_library_json)
        settings.add_json_panel('Playback', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_playback_json)

    def on_config_change(self, config, section, key, value):
        common_global.es_inst.com_elastic_index('info', {'config': config, 'section': section,
                                                         'key': key, 'value':
                                                             value})

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

    def theater_event_button_user_select_login(self, *args):
        self.dismiss_popup()
        common_global.es_inst.com_elastic_index('info', {"button server user login":
                                                             self.global_selected_user_id})
        common_global.es_inst.com_elastic_index('info', {"login": self.login_password})
        self.send_twisted_message(json.dumps({'Type': 'Login',
                                              'User': self.global_selected_user_id,
                                              'Password': self.login_password}))
        self.root.ids._screen_manager.current = 'Main_Remote'

    def main_mediakraken_event_button_home(self, *args):
        msg = json.dumps({'Type': 'Media', 'Sub': 'List', 'Data': args[0]})
        common_global.es_inst.com_elastic_index('info', {"home press": args})
        if args[0] == 'in_progress' or args[0] == 'recent_addition' \
                or args[0] == 'Movie' or args[0] == 'video':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_List'
        elif args[0] == 'demo':
            # add movie id to stream
            try:
                msg += " " + self.demo_media_id
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
            except:
                msg = None
        else:
            common_global.es_inst.com_elastic_index('error', {'stuff': "unknown button event"})
        if msg is not None:
            self.send_twisted_message(msg)

    def theater_event_button_option_select(self, option_text, *args):
        common_global.es_inst.com_elastic_index('info', {"button server options": option_text})
        if option_text == 'Audio Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Audio'
        elif option_text == 'Playback Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Playback'
        elif option_text == 'Video Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Video'

    # send refresh for images
    def main_image_refresh(self, *largs):
        common_global.es_inst.com_elastic_index('info', {'stuff': "image refresh"})
        # if main page refresh all images
        if self.root.ids._screen_manager.current == 'Main_Theater_Home':
            # refreshs for movie stuff
            # request main screen background refresh
            self.send_twisted_message(json.dumps({'Type': 'Image', 'Sub': 'Movie',
                                                  'Sub2': 'Demo', 'Sub3': 'Backdrop'}))

    def _image_loaded_home_demo(self, proxyImage):
        """
        Load home image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_demo_image.texture = proxyImage.image.texture
        # since it's loaded delete the image
        os.remove('./image_demo')


if __name__ == '__main__':
    # for windows exe support
    from multiprocessing import freeze_support

    freeze_support()
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
        'main_theater_thin')

    log.startLogging(sys.stdout)  # for twisted
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # load the kivy's here so all the classes have been defined
    Builder.load_file('theater_thin/kivy_layouts/main.kv')
    Builder.load_file('theater_thin/kivy_layouts/KV_Layout_Notification.kv')
    # so the raspberry pi doesn't crash
    if os.uname()[4][:3] != 'arm':
        Window.fullscreen = 'auto'
    MediaKrakenApp().run()
