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

import base64
import json
import logging  # pylint: disable=W0611
import os
import platform
import subprocess
import sys
import uuid
from shlex import split

from common import common_global
from common import common_logging_elasticsearch
from common import common_network_mediakraken
from common import common_network_mpv
from common import common_signal
from common import common_theater

logging.getLogger('twisted').setLevel(logging.ERROR)
from functools import partial

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
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithSidebar
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ObjectProperty
from theater import MediaKrakenSettings

twisted_connection = None
mk_app = None


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print(("selection changed to {0}".format(rv.data[index])))
            MKFactory.protocol.sendline_data(twisted_connection,
                                             json.dumps({'Type': 'Media', 'Subtype': 'Detail',
                                                         'UUID': rv.data[index]['uuid']}))
            common_global.es_inst.com_elastic_index('info', {'stuff': rv.data[index]['path']})
            MediaKrakenApp.media_path = rv.data[index]['path']


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


class MediaKrakenLoadDialog(FloatLayout):
    """
    Load file dialog
    """
    load = ObjectProperty(None)
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

    def show_load(self):
        content = MediaKrakenLoadDialog(
            load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load media file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_popup()

    def mediakraken_find_server_list(self):
        self.server_list = common_network_mediakraken.com_net_mediakraken_find_server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1],
                                    group='mediakraken_server', )
                btn1.bind(on_press=partial(self.MediaKraken_Event_Button_Server_Select,
                                           found_server))
                self.root.ids.mediakraken_server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'

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
        self.common_remote = common_theater.main_remote_control_event_process
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
                common_global.es_inst.com_elastic_index('info', {'server list':
                                                                     server_list})
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
                common_global.es_inst.com_elastic_index('info', {'Got Message': server_msg})
            else:
                common_global.es_inst.com_elastic_index('info', {'Got Image Message':
                                                                     json_message['Sub'], 'UUID':
                                                                     json_message['UUID']})
        except:
            common_global.es_inst.com_elastic_index('info', {'full record': server_msg})
        common_global.es_inst.com_elastic_index('info', {'len total': len(server_msg)})
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident',
                                                         'UUID': str(uuid.uuid4()),
                                                         'Platform': platform.node()}))
            # start up the image refresh since we have a connection
            Clock.schedule_interval(self.main_image_refresh, 5.0)
        elif json_message['Type'] == "Media":
            if json_message['Subtype'] == "Detail":
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
                # "LocalImages": {"Banner": "", "Fanart": "",
                # "Poster": "../images/poster/f/9mhyID0imBjaRj3FJkARuXXSiQU.jpg", "Backdrop": null},
                production_list = ''
                for ndx in range(0, len(json_message['Data']['Meta']['themoviedb']['Meta'][
                                            'production_companies'])):
                    production_list += (json_message['Data']['Meta']['themoviedb']['Meta'][
                                            'production_companies'][ndx]['name'] + ', ')
                self.root.ids.theater_media_video_production_companies.text = production_list[
                                                                              :-2]
                # go through streams
                audio_streams = []
                subtitle_streams = ['None']
                if json_message['Data2'] is not None and 'FFprobe' in json_message['Data2'] \
                        and 'streams' in json_message['Data2']['FFprobe'] \
                        and json_message['Data2']['FFprobe']['streams'] is not None:
                    for stream_info in json_message['Data2']['FFprobe']['streams']:
                        common_global.es_inst.com_elastic_index('info',
                                                                {'info': stream_info})
                        stream_language = ''
                        stream_title = ''
                        stream_codec = ''
                        try:
                            stream_language = stream_info['tags']['language'] + ' - '
                        except:
                            pass
                        try:
                            stream_title = stream_info['tags']['title'] + ' - '
                        except:
                            pass
                        try:
                            stream_codec \
                                = stream_info['codec_long_name'].rsplit('(', 1)[1].replace(')', '') \
                                  + ' - '
                        except:
                            pass
                        if stream_info['codec_type'] == 'audio':
                            common_global.es_inst.com_elastic_index('info', {'stuff': 'audio'})
                            audio_streams.append((stream_codec + stream_language
                                                  + stream_title)[:-3])
                        elif stream_info['codec_type'] == 'subtitle':
                            subtitle_streams.append(stream_language)
                            common_global.es_inst.com_elastic_index('info', {'stuff': 'subtitle'})
                # populate the audio streams to select
                self.root.ids.theater_media_video_audio_spinner.values = list(map(
                    str, audio_streams))
                self.root.ids.theater_media_video_audio_spinner.text = 'None'
                # populate the subtitle options
                self.root.ids.theater_media_video_subtitle_spinner.values = list(map(str,
                                                                                     subtitle_streams))
                self.root.ids.theater_media_video_subtitle_spinner.text = 'None'
                #            # populate the chapter grid
                #            for chapter_info in json_message['FFprobe']['chapters']:
                #                # media_json['ChapterImages']
                #                chapter_box = BoxLayout(size_hint_y=None)
                #                chapter_label = Label(text='Test Chapter')
                #                chapter_label_start = Label(text='Start Time')
                #                chapter_image = Image(source='./images/3D.png')
                #                chapter_box.add_widget(chapter_label)
                #                chapter_box.add_widget(chapter_label)
                #                chapter_box.add_widget(chapter_image)
                #                self.root.ids.theater_media_video_chapter_grid.add_widget(chapter_box)
            elif json_message['Sub'] == "List":
                data = []
                for video_list in json_message['Data']:
                    data.append({'text': video_list[0], 'uuid': video_list[1],
                                 'path': video_list[4]})
                self.root.ids.theater_media_video_list_scrollview.data = data
        elif json_message['Type'] == 'Play':  # direct file play
            # AttributeError: 'NoneType' object has no attribute
            # 'set_volume'  <- means can't find file
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
            video_source_dir = json_message['Data']
            share_mapping = (
                ('/mediakraken/mnt/zfsspoo/', '/home/spoot/zfsspoo/'),)
            if share_mapping is not None:
                for mapping in share_mapping:
                    video_source_dir = video_source_dir.replace(
                        mapping[0], mapping[1])
            self.root.ids.theater_media_video_videoplayer.source = video_source_dir
            self.root.ids.theater_media_video_videoplayer.volume = 1
            self.root.ids.theater_media_video_videoplayer.state = 'play'
        # after connection receive the list of users to possibly login with
        elif json_message['Type'] == "User":
            pass
        elif json_message['Type'] == "Genre List":
            common_global.es_inst.com_elastic_index('info', {'stuff': "gen"})
            for genre_list in json_message:
                common_global.es_inst.com_elastic_index('info', {"genlist": genre_list})
                btn1 = ToggleButton(text=genre_list[0], group='button_group_genre_list',
                                    size_hint_y=None,
                                    width=self.root.ids.theater_media_genre_list_scrollview.width,
                                    height=(
                                            self.root.ids.theater_media_genre_list_scrollview.height / 8))
                btn1.bind(on_press=partial(
                    self.Theater_Event_Button_Genre_Select, genre_list[0]))
                self.root.ids.theater_media_genre_list_scrollview.add_widget(
                    btn1)
        elif json_message['Type'] == "Image":
            if json_message['Sub'] == "Movie":
                common_global.es_inst.com_elastic_index('info', {'stuff': "here for movie refresh"})
                f = open('./image_demo', "w")
                f.write(base64.b64decode(json_message['Data']))
                f.close()
                self.demo_media_id = json_message['UUID']
                proxy_image_demo = Loader.image('./image_demo')
                proxy_image_demo.bind(on_load=self._image_loaded_home_demo)
            elif json_message['Sub2'] == "Movie":
                f = open('./image_movie', "w")
                f.write(base64.b64decode(json_message['Data']))
                f.close()
                proxy_image_movie = Loader.image('./image_movie')
                proxy_image_movie.bind(
                    on_load=self._image_loaded_home_movie)
            elif json_message['Sub2'] == "New Movie":
                f = open('./image_new_movie', "w")
                f.write(base64.b64decode(json_message['Data']))
                f.close()
                proxy_image_new_movie = Loader.image('./image_new_movie')
                proxy_image_new_movie.bind(
                    on_load=self._image_loaded_home_new_movie)
            elif json_message['Sub2'] == "In Progress":
                f = open('./image_in_progress', "w")
                f.write(base64.b64decode(json_message['Data']))
                f.close()
                proxy_image_prog_movie = Loader.image('./image_in_progress')
                proxy_image_prog_movie.bind(
                    on_load=self._image_loaded_home_prog_movie)
                # elif pickle_data[0] == "MOVIEDETAIL":
                #     common_global.es_inst.com_elastic_index('info', {'stuff':"here for movie detail refresh: %s", pickle_data[1])
                #     proxy_image_detail_movie = Loader.image(pickle_data[1])
                #     proxy_image_detail_movie.bind(on_load=self._image_loaded_detail_movie)
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
    common_global.es_inst.com_elastic_index('info', {'stuff': {'config': config,
                                                               'section': section,
                                                               'key': key,
                                                               'value': value}})

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        common_global.es_inst.com_elastic_index('info', {"keycode received": keycode})
        if keycode[1] == 'i' or keycode[1] == 'I':
            if self.root.ids._screen_manager.current == 'Main_Theater_Media_Playback':
                # show media information overlay
                pass
        elif keycode[1] == 'up':
            if self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List':
                # scroll up a page of media
                pass
            elif self.root.ids._screen_manager.current == 'Main_Theater_Home':
                # scroll up an icon
                pass
        elif keycode[1] == 'down':
            if self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List':
                # scroll down a page of media
                pass
            elif self.root.ids._screen_manager.current == 'Main_Theater_Home':
                # scroll down an icon
                pass
        elif keycode[1] == 'left':
            if self.root.ids._screen_manager.current == 'Main_Theater_Home':
                # scroll left an icon
                pass
        elif keycode[1] == 'right':
            if self.root.ids._screen_manager.current == 'Main_Theater_Home':
                # scroll left an icon
                pass
        elif keycode[1] == 'backspace':
            if self.root.ids._screen_manager.current == 'Main_Theater_Home':
                pass
            elif self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_Detail':
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_List'
            elif self.root.ids._screen_manager.current == 'Main_Theater_Media_Playback':
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_Detail'
            elif self.root.ids._screen_manager.current == 'Main_Theater_Media_TV_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_LIVE_TV_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Images_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Game_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Books_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Radio_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Music_Video_List' \
                    or self.root.ids._screen_manager.current == 'Main_Theater_Media_Music_List':
                self.root.ids._screen_manager.current = 'Main_Theater_Home'
            pass
        elif keycode[1] == 'enter':
            pass
        elif keycode[1] == 'shift':
            pass
        elif keycode[1] == 'rshift':
            pass
        elif keycode[1] == 'lctrl':
            pass
        elif keycode[1] == 'rctrl':
            pass
        elif keycode[1] == 'alt':
            pass
        elif keycode[1] == 'alt-gr':
            pass
        elif keycode[1] == 'tab':
            pass
        elif keycode[1] == 'escape':
            sys.exit()
        elif keycode[1] == 'home':
            self.root.ids._screen_manager.current = 'Main_Theater_Home'
        elif keycode[1] == 'end':
            pass
        elif keycode[1] == 'pageup':
            if self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List':
                # scroll up a page of media
                self.root.ids.theater_media_video_list_scrollview.scroll_y = 0
        elif keycode[1] == 'pagedown':
            if self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List':
                # scroll down a page of media
                self.root.ids.theater_media_video_list_scrollview.scroll_y = 1
        elif keycode[1] == 'insert':
            pass
        elif keycode[1] == 'delete':
            pass
        elif keycode[1] == 'f1':
            # display help
            pass
        return True

    # play media from movie section
    def main_mediakraken_event_play_media_mpv(self, *args):
        common_global.es_inst.com_elastic_index('info', {'stuff': MediaKrakenApp.media_path})
        if self.root.ids.theater_media_video_play_local_spinner.text == 'This Device':
            if os.path.isfile(MediaKrakenApp.media_path):
                self.mpv_process = subprocess.Popen(
                    split('mpv --no-config --fullscreen --ontop --no-osc --no-osd-bar --aid=2',
                          '--audio-spdif=ac3,dts,dts-hd,truehd,eac3 --audio-device=pulse',
                          '--hwdec=auto --input-ipc-server ./mk_mpv.sock \"'
                          + MediaKrakenApp.media_path + '\"'))
                self.mpv_connection = common_network_mpv.CommonNetMPVSocat()
            else:
                self.theater_play_server()
        else:
            self.theater_play_server()
            self.root.ids._screen_manager.current = 'Main_Theater_Remote'

    def theater_play_server(self):
        # the server will have the target device....to know if cast/stream/etc
        self.send_twisted_message(json.dumps({'Type': 'Play', 'Subtype': 'Client',
                                              'Media UUID': MediaKrakenApp.media_uuid,
                                              'Target': self.root.ids.theater_media_video_play_local_spinner.text}))

    # genre select
    def Theater_Event_Button_Genre_Select(self, *args):
        common_global.es_inst.com_elastic_index('info', {"genre select": args})
        self.media_genre = args[0]
        self.send_twisted_message(("VIDEOGENRELIST " + args[0]))

    def theater_event_button_user_select_login(self, *args):
        self.dismiss_popup()
        common_global.es_inst.com_elastic_index('info', {"button server user login":
                                                             self.global_selected_user_id})
        common_global.es_inst.com_elastic_index('info', {"login": self.login_password})
        self.send_twisted_message(json.dumps({'Type': 'Login',
                                              'User': self.global_selected_user_id,
                                              'Password': self.login_password}))
        self.root.ids._screen_manager.current = 'Main_Remote'

    def main_mediakraken_event_button_video_play(self, *args):
        common_global.es_inst.com_elastic_index('info', {"play": args})
        msg = "demo " + self.media_guid
        self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
        self.send_twisted_message(msg)

    def main_mediakraken_event_button_home(self, *args):
        msg = json.dumps({'Type': 'Media', 'Subtype': 'List', 'Data': args[0]})
        common_global.es_inst.com_elastic_index('info', {'stuff': "home press: %s" % args})
        if args[0] == 'in_progress' or args[0] == 'recent_addition' \
                or args[0] == 'Movie' or args[0] == 'video':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_List'
        elif args[0] == 'tv':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_TV_List'
        elif args[0] == 'games':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Game_List'
        elif args[0] == 'music_vid':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Music_Video_List'
        elif args[0] == 'demo':
            # add movie id to stream
            try:
                msg += " " + self.demo_media_id
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
            except:
                msg = None
        elif args[0] == 'pictures':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Images_List'
        elif args[0] == 'radio':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Radio_List'
        elif args[0] == 'periodicals':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Books_List'
        elif args[0] == 'music':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Music_List'
        elif args[0] == 'live':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_LIVE_TV_List'
        else:
            common_global.es_inst.com_elastic_index('error', {'stuff': "unknown button event"})
            if msg is not None:
                self.send_twisted_message(msg)

    def theater_event_button_option_select(self, option_text, *args):
        common_global.es_inst.com_elastic_index('info',
                                                {'stuff': "button server options %s" % option_text})
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
            self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Movie',
                                                  'Image Media Type': 'Demo',
                                                  'Image Type': 'Backdrop'}))
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Movie',
                                              'Image Media Type': 'Movie',
                                              'Image Type': 'Backdrop'}))
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Movie',
                                              'Image Media Type': 'New Movie',
                                              'Image Type': 'Backdrop'}))
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Movie',
                                              'Image Media Type': 'In Progress',
                                              'Image Type': 'Backdrop'}))
        # refreshs for tv stuff
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'TV',
                                              'Image Media Type': 'TV', 'Image Type': 'Backdrop'}))
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'TV',
                                              'Image Media Type': 'Live TV',
                                              'Image Type': 'Backdrop'}))
        # refreshs for game stuff
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Game',
                                              'Image Media Type': 'Game',
                                              'Image Type': 'Backdrop'}))
        # refreshs for books stuff
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Book',
                                              'Image Media Type': 'Book', 'Image Type': 'Cover'}))
        # refresh music stuff
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Music',
                                              'Image Media Type': 'Album', 'Image Type': 'Cover'}))
        # request main screen background refresh
        self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Music',
                                              'Image Media Type': 'Video',
                                              'Image Type': 'Backdrop'}))
        # refresh image stuff
        # request main screen background refresh
        # self.send_twisted_message("IMAGE IMAGE IMAGE None Backdrop")
        # self.send_twisted_message({'Type': 'Image', 'Subtype': 'Image Media Type', 'Data': 'Game', 'Image Type': 'Backdrop'})

    def _image_loaded_detail_movie(self, proxyImage):
        """
        Load movie image
        """
        if proxyImage.image.texture:
            self.root.ids.theater_media_video_poster.texture = proxyImage.image.texture

    def _image_loaded_home_demo(self, proxyImage):
        """
        Load home image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_demo_image.texture = proxyImage.image.texture
        # since it's loaded delete the image
        # os.remove(self.home_demo_file_name)

    def _image_loaded_home_movie(self, proxyImage):
        """
        Load home movie image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_movie_image.texture = proxyImage.image.texture
        # since it's loaded delete the image
        # os.remove(self.home_movie_file_name)

    def _image_loaded_home_new_movie(self, proxyImage):
        """
        Load new movie image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_new_movie_image.texture = proxyImage.image.texture
        # since it's loaded delete the image
        # os.remove(self.home_movie_new_file_name)

    def _image_loaded_home_prog_movie(self, proxyImage):
        """
        Load in progress movie image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_progress_movie_image.texture = proxyImage.image.texture
        # since it's loaded delete the image
        # os.remove(self.home_movie_inprogress_file_name)

    if __name__ == '__main__':
        # for windows exe support
        from multiprocessing import freeze_support

        freeze_support()
        # start logging
        common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_theater')
        log.startLogging(sys.stdout)  # for twisted
        # set signal exit breaks
        common_signal.com_signal_set_break()
        # load the kivy's here so all the classes have been defined
        Builder.load_file('theater/kivy_layouts/main.kv')
        Builder.load_file('theater/kivy_layouts/KV_Layout_Load_Dialog.kv')
        Builder.load_file('theater/kivy_layouts/KV_Layout_Login.kv')
        Builder.load_file('theater/kivy_layouts/KV_Layout_Notification.kv')
        Builder.load_file('theater/kivy_layouts/KV_Layout_Slider.kv')
        # so the raspberry pi doesn't crash
        if os.uname()[4][:3] != 'arm':
            Window.fullscreen = 'auto'
        MediaKrakenApp().run()
