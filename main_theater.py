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
from common import common_logging
from common import common_signal
import platform
try:
    import cPickle as pickle
except:
    import pickle
import logging # pylint: disable=W0611
from functools import partial

# install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.lang import Builder

# A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol
from twisted.internet import ssl


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        self.factory.app.process_message(data)
        logging.info(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        #self.app.print_message("connection lost")
        logging.info('connection lost')

    def clientConnectionFailed(self, conn, reason):
        #self.app.print_message("connection failed")
        logging.info('connection failed')


import kivy
from kivy.app import App
kivy.require('1.9.2')
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
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
from theater import MediaKrakenSettings


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
    connection = None

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
        root = MediaKraken()
        self.config = self.load_config()
        self.settings_cls = SettingsWithSidebar
        # turn off the kivy panel settings
        self.use_kivy_settings = False
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.connect_to_server()
        return root

    def connect_to_server(self):
        logging.info('conn server')
        if self.config is not None:
            logging.info('here in connect to server')
            reactor.connectSSL(self.config.get('MediaKrakenServer', 'Host').strip(),
                int(self.config.get('MediaKrakenServer', 'Port').strip()),
                EchoFactory(self), ssl.ClientContextFactory())

    def on_connection(self, connection):
        logging.info("connected successfully!")
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def process_message(self, server_msg):
        """
        Process network message from server
        """
        # otherwise the pickle can end up in thousands of chunks
        message_words = server_msg.split(' ', 1)
        if message_words[0] != "IMAGE":
            logging.info("Got Message: %s", server_msg)
        logging.info('message: %s', message_words[0])
        logging.info('len header: %s', len(message_words[0]))
        logging.info("len total: %s", len(server_msg))
        logging.info("chunks: %s", len(message_words))
        try:
            pickle_data = pickle.loads(message_words[1])
        except:
            pickle_data = None
        if message_words[0] == "IDENT":
            self.connection.write(("VALIDATE " + "admin" + " " + "password" + " "
                                 + platform.node()).encode("utf8"))
            # start up the image refresh since we have a connection
            Clock.schedule_interval(self.main_image_refresh, 5.0)
        # after login receive the list of users to possibly login with
        elif message_words[0] == "USERLIST":
            pass
        elif message_words[0] == 'VIDPLAY':
            # AttributeError: 'NoneType' object has no attribute
            # 'set_volume'  <- means can't find file
            self.root.ids.theater_media_video_videoplayer.source = message_words[1]
            self.root.ids.theater_media_video_videoplayer.volume = 1
            self.root.ids.theater_media_video_videoplayer.state = 'play'
        elif message_words[0] == "VIDEOLIST":
            if pickle_data is not None:
                data = [{'text': str(i), 'is_selected': False} for i in range(100)]
                args_converter = lambda row_index, \
                                        rec: {'text': rec['text'], 'size_hint_y': None, 'height': 25}
                list_adapter = ListAdapter(data=data, args_converter=args_converter,
                                           cls=ListItemButton, selection_mode='single', allow_empty_selection=False)
                list_view = ListView(adapter=list_adapter)
                for video_list in pickle_data:
                    btn1 = ToggleButton(text=video_list[0], group='button_group_video_list',
                                        size_hint_y=None,
                                        width=self.root.ids.theater_media_video_list_scrollview.width,
                                        height=(self.root.ids.theater_media_video_list_scrollview.height / 8))
                    btn1.bind(on_press=partial(self.theater_event_button_video_select, video_list[1]))
                    self.root.ids.theater_media_video_list_scrollview.add_widget(btn1)
        elif message_words[0] == "VIDEODETAIL":
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_Detail'
            # load vid detail
            # mm_media_name,mm_media_ffprobe_json,mm_media_json,mm_metadata_json
            ffprobe_json = pickle_data[1]
            media_json = pickle_data[2]
            metadata_json = pickle_data[3]
            self.root.ids.theater_media_video_title.text = pickle_data[0]
            self.root.ids.theater_media_video_subtitle.text = metadata_json['tagline']
            # self.root.ids.theater_media_video_rating = row_data[3]['']
            self.root.ids.theater_media_video_runtime.text = str(metadata_json['runtime'])
            self.root.ids.theater_media_video_overview.text = metadata_json['overview']
            genres_list = ''
            for ndx in range(0, len(metadata_json['genres'])):
                genres_list += (metadata_json['genres'][ndx]['name'] + ', ')
            self.root.ids.theater_media_video_genres.text = genres_list[:-2]
            # "LocalImages": {"Banner": "", "Fanart": "",
            # "Poster": "../images/poster/f/9mhyID0imBjaRj3FJkARuXXSiQU.jpg", "Backdrop": null},
            production_list = ''
            for ndx in range(0, len(metadata_json['production_companies'])):
                production_list += (metadata_json['production_companies'][ndx]['name'] + ', ')
            self.root.ids.theater_media_video_production_companies.text = production_list[:-2]
            # go through streams
            audio_streams = []
            subtitle_streams = ['None']
            for stream_info in ffprobe_json['streams']:
                logging.info("info: %s", stream_info)
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
                        = stream_info['codec_long_name'].rsplit('(', 1)[1].replace(')', '') + ' - '
                except:
                    pass
                if stream_info['codec_type'] == 'audio':
                    logging.info('audio')
                    audio_streams.append((stream_codec + stream_language + stream_title)[:-3])
                elif stream_info['codec_type'] == 'subtitle':
                    subtitle_streams.append(stream_language)
                    logging.info('sub')
            # populate the audio streams to select
            self.root.ids.theater_media_video_audio_spinner.values = map(str, audio_streams)
            self.root.ids.theater_media_video_audio_spinner.text = 'None'
            # populate the subtitle options
            self.root.ids.theater_media_video_subtitle_spinner.values = map(str, subtitle_streams)
            self.root.ids.theater_media_video_subtitle_spinner.text = 'None'
            #            # populate the chapter grid
            #            for chapter_info in ffprobe_json['chapters']:
            #                # media_json['ChapterImages']
            #                chapter_box = BoxLayout(size_hint_y=None)
            #                chapter_label = Label(text='Test Chapter')
            #                chapter_label_start = Label(text='Start Time')
            #                chapter_image = Image(source='./images/3D.png')
            #                chapter_box.add_widget(chapter_label)
            #                chapter_box.add_widget(chapter_label)
            #                chapter_box.add_widget(chapter_image)
            #                self.root.ids.theater_media_video_chapter_grid.add_widget(chapter_box)
        elif message_words[0] == "ALBUMLIST":
            pass
        elif message_words[0] == "ALBUMDETAIL":
            pass
        elif message_words[0] == "MUSICLIST":
            pass
        elif message_words[0] == "AUDIODETAIL":
            pass
        elif message_words[0] == "GENRELIST":
            logging.info("gen")
            for genre_list in pickle_data:
                logging.info("genlist: %s", genre_list)
                btn1 = ToggleButton(text=genre_list[0], group='button_group_genre_list',
                                    size_hint_y=None,
                                    width=self.root.ids.theater_media_genre_list_scrollview.width,
                                    height=(self.root.ids.theater_media_genre_list_scrollview.height / 8))
                btn1.bind(on_press=partial(self.Theater_Event_Button_Genre_Select, genre_list[0]))
                self.root.ids.theater_media_genre_list_scrollview.add_widget(btn1)
        elif message_words[0] == "PERSONLIST":
            pass
        elif message_words[0] == "PERSONDETAIL":
            pass
        # metadata images
        elif message_words[0] == "IMAGE":
            if pickle_data[0] == "MAIN":
                logging.info("here for main refresh: %s %s", pickle_data[1], pickle_data[2])
                self.demo_media_id = pickle_data[2]
                proxy_image_demo = Loader.image(pickle_data[1])
                proxy_image_demo.bind(on_load=self._image_loaded_home_demo)
            elif pickle_data[0] == "MOVIE":
                logging.info("here for movie refresh: %s", pickle_data[1])
                proxy_image_movie = Loader.image(pickle_data[1])
                proxy_image_movie.bind(on_load=self._image_loaded_home_movie)
            elif pickle_data[0] == "NEWMOVIE":
                logging.info("here for newmovie refresh: %s", pickle_data[1])
                proxy_image_new_movie = Loader.image(pickle_data[1])
                proxy_image_new_movie.bind(on_load=self._image_loaded_home_new_movie)
            elif pickle_data[0] == "PROGMOVIE":
                logging.info("here for progress movie refresh: %s", pickle_data[1])
                proxy_image_prog_movie = Loader.image(pickle_data[1])
                proxy_image_prog_movie.bind(on_load=self._image_loaded_home_prog_movie)
            elif pickle_data[0] == "MOVIEDETAIL":
                logging.info("here for movie detail refresh: %s", pickle_data[1])
                proxy_image_detail_movie = Loader.image(pickle_data[1])
                proxy_image_detail_movie.bind(on_load=self._image_loaded_detail_movie)
        else:
            logging.error("unknown message type")

    def build_config(self, config):
        """
        Build base config
        """
        config.setdefaults('MediaKrakenServer', {
            'Host': '10.1.0.187',
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
        logging.info("%s %s %s %s", config, section, key, value)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        logging.info("keycode received: %s", keycode)
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
            elif self.root.ids._screen_manager.current == 'Main_Theater_Media_TV_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Video_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_LIVE_TV_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Images_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Game_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Books_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Radio_List'\
                or self.root.ids._screen_manager.current == 'Main_Theater_Media_Music_Video_List'\
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
            self.root.ids._screen_manager.current = 'Main_Theater_Home'
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

    # video select
    def theater_event_button_video_select(self, *args):
        logging.info("vid select: %s", args)
        self.media_guid = args[0]
        self.connection.write(("VIDEODETAIL " + args[0]).encode("utf8"))
        # grab poster
        # request main screen background refresh
        self.connection.write(("IMAGE MOVIEDETAIL MOVIE " + args[0]).encode("utf8"))

    # genre select
    def Theater_Event_Button_Genre_Select(self, *args):
        logging.info("genre select: %s", args)
        self.media_genre = args[0]
        self.connection.write(("VIDEOGENRELIST " + args[0]).encode("utf8"))

    def theater_event_button_user_select_login(self, *args):
        self.dismiss_popup()
        logging.info("button server user login %s", self.global_selected_user_id)
        logging.info("login: %s", self.login_password)
        self.connection.write("LOGIN " + self.global_selected_user_id + " " + self.login_password)
        self.root.ids._screen_manager.current = 'Main_Remote'

    def main_mediakraken_event_button_video_play(self, *args):
        logging.info("play: %s", args)
        msg = "demo " + self.media_guid
        self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
        self.connection.write(msg.encode("utf8"))

    def main_mediakraken_event_button_home(self, *args):
        global network_protocol
        msg = args[0]
        logging.info("home press: %s", args)
        if args[0] == 'in_progress' or args[0] == 'recent_addition'\
                or args[0] == 'movie' or args[0] == 'video':
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
            logging.error("unknown button event")
        if msg is not None:
            self.connection.write(msg.encode("utf8"))

    def theater_event_button_option_select(self, option_text, *args):
        logging.info("button server options %s", option_text)
        if option_text == 'Audio Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Audio'
        elif option_text == 'Playback Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Playback'
        elif option_text == 'Video Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Video'

    # send refresh for images
    def main_image_refresh(self, *largs):
        logging.info("image refresh")
        # if main page refresh all images
        if self.root.ids._screen_manager.current == 'Main_Theater_Home':
            # refreshs for movie stuff
            # request main screen background refresh
            self.connection.write("IMAGE MAIN MOVIE None Backdrop".encode("utf8"))
            # request main screen background refresh
            self.connection.write("IMAGE MOVIE MOVIE None Backdrop".encode("utf8"))
            # request main screen background refresh
            self.connection.write("IMAGE NEWMOVIE MOVIE None Backdrop".encode("utf8"))
            # request main screen background refresh
            self.connection.write("IMAGE PROGMOVIE MOVIE None Backdrop".encode("utf8"))
            # refreshs for tv stuff
            # request main screen background refresh
            self.connection.write("IMAGE TV TVSHOW None Backdrop".encode("utf8"))
            # request main screen background refresh
            self.connection.write("IMAGE LIVETV TVLIVE None Backdrop".encode("utf8"))
            # refreshs for game stuff
            # request main screen background refresh
            self.connection.write("IMAGE GAME VIDEOGAME None Backdrop".encode("utf8"))
            # refreshs for books stuff
            # request main screen background refresh
            self.connection.write("IMAGE BOOK BOOK None Backdrop".encode("utf8"))
            # refresh music stuff
            # request main screen background refresh
            self.connection.write("IMAGE MUSICALBUM MUSIC None Backdrop".encode("utf8"))
            # request main screen background refresh
            self.connection.write("IMAGE MUSICVIDEO MUSIC None Backdrop".encode("utf8"))
            # refresh image stuff
            # request main screen background refresh
            self.connection.write("IMAGE IMAGE IMAGE None Backdrop".encode("utf8"))

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

    def _image_loaded_home_movie(self, proxyImage):
        """
        Load home movie image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_movie_image.texture = proxyImage.image.texture

    def _image_loaded_home_new_movie(self, proxyImage):
        """
        Load new movie image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_new_movie_image.texture = proxyImage.image.texture

    def _image_loaded_home_prog_movie(self, proxyImage):
        if proxyImage.image.texture:
            self.root.ids.main_home_progress_movie_image.texture = proxyImage.image.texture

if __name__ == '__main__':
    common_logging.com_logging_start('./log/MediaKraken_Theater')
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # load the kivy's here so all the classes have been defined
    Builder.load_file('theater/kivy_layouts/main.kv')
    Builder.load_file('theater/kivy_layouts/KV_Layout_Load_Dialog.kv')
    Builder.load_file('theater/kivy_layouts/KV_Layout_Login.kv')
    Builder.load_file('theater/kivy_layouts/KV_Layout_Notification.kv')
    Builder.load_file('theater/kivy_layouts/KV_Layout_Slider.kv')
    MediaKrakenApp().run()
