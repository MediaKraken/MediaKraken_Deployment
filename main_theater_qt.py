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
import json
import os
import sys
import base64
import uuid
import platform
import subprocess
from PyQt5.QtCore import Qt
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QDialog, QApplication
import PyQt5.QtWidgets as QtWidgets
sys.path.append('theater_qt')
from common import common_file
from common import common_logging
from common import common_network_mpv
from common import common_network_mediakraken
from common import common_version
from ui import mk_browse_movie_ui
from ui import mk_login_ui
from ui import mk_mainwindow_ui
from ui import mk_player_ui
from theater_qt import MediaKrakenSettings
from twisted.internet import protocol
from twisted.protocols import basic
from twisted.internet import ssl
from twisted.python import log

twisted_connection = None
mk_app = None


class PlayerUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PlayerUI, self).__init__(parent)
        self.ui = mk_player_ui.ui.player_ui.Ui_Player()
        self.ui.setupUi(self)
        self.ui.player_widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)
        self.ui.player_widget.setAttribute(QtCore.Qt.WA_NativeWindow)
        self.ui.player_widget.setMouseTracking(True)
        self.ui.slider_volume.setMaximum(100)
        self.ui.audio_tracks.set_type('audio')
        self.ui.sub_tracks.set_type('sub')


class ComponentWindow(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal(str)

    def __init__(self, name, parent=None):
        super(ComponentWindow, self).__init__(parent)
        self.name = name

    def _shutdown(self):
        self.closed.emit(self.name)


class MPVPlayer(ComponentWindow):

    def __init__(self, name, parent=None):
        super(MPVPlayer, self).__init__(name, parent)
        self.ui = PlayerUI(self)
        self.setCentralWidget(self.ui)
        self.mpv_pid = subprocess.Popen(['mpv', '--wid', int(self.ui.player.winId()),
                                         '--hwdec=auto', '--input-ipc-server' './mk_mpv.sock'])
        self.mpv_ipc = common_network_mpv.CommonNetMPV()


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
        MainWindow.process_message(mk_app, line)

    def connectionLost(self, reason):
        logging.error("connection lost!")
        #reactor.stop() # leave out so it doesn't try to stop a stopped reactor

    def sendline_data(self, line):
        logging.info('sending: %s', line)
        self.sendLine(line.encode("utf8"))


class MKFactory(protocol.ClientFactory):
    protocol = MKEcho


class PlayerWindow(QMainWindow, mk_player_ui.Ui_MK_Player):
    def __init__(self, parent=None):
        super(PlayerWindow, self).__init__(parent)
        self.setupUi(self)


class LoginDialog(QDialog, mk_login_ui.Ui_MK_Login):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)


class BrowseMovieWindow(QMainWindow, mk_browse_movie_ui.Ui_MK_Browse_Movie):
    def __init__(self, parent=None):
        super(BrowseMovieWindow, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow, mk_mainwindow_ui.Ui_MK_MainWindow):
    global twisted_connection
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.main_button_books.clicked.connect(self.main_button_books_clicked)
        self.main_button_home_movie.clicked.connect(self.main_button_home_movie_clicked)
        self.main_button_images.clicked.connect(self.main_button_images_clicked)
        self.main_button_movie.clicked.connect(self.main_button_movie_clicked)
        self.main_button_music.clicked.connect(self.main_button_music_clicked)
        self.main_button_radio.clicked.connect(self.main_button_radio_clicked)
        self.main_button_settings.clicked.connect(self.main_button_settings_clicked)
        self.main_button_tv.clicked.connect(self.main_button_tv_clicked)
        self.main_button_tv_live.clicked.connect(self.main_button_tv_live_clicked)
        self.setWindowTitle('MediaKraken ' + common_version.APP_VERSION)
        # setup the other windows (this way only done once to negate memory leak)
        self.window_browse_movie = BrowseMovieWindow(self)
        self.window_login = LoginDialog(self)
        self.window_player = PlayerWindow(self)
        # load config
        if os.path.isfile('./conf/mk_theater.cfg'):
            pass
        else:
            config_json = MediaKrakenSettings.mediakraken_settings_base_json
            common_file.com_file_save_data('./conf/mk_theater.cfg', json.dumps(config_json), True)
        self.mk_config = json.loads(common_file.com_file_load_data('./conf/mk_theater.cfg', True))
        global mk_app
        mk_app = self
        # attempt server connect
        self.connect_to_server()

    def connect_to_server(self):
        logging.info('conn server')
        print(self.mk_config)
        if self.mk_config['MediaKrakenServer']['Host'] is None:
            # TODO if more than one server, popup list selection
            server_list = common_network_mediakraken.com_net_mediakraken_find_server()
            logging.info('server list: %s', server_list)
            host_ip = server_list[0]
            # TODO allow pick from list and save it below
            self.mk_config['MediaKrakenServer']['Host'] = host_ip.split(':')[0]
            self.mk_config['MediaKrakenServer']['Port'] = host_ip.split(':')[1]
            common_file.com_file_save_data('./conf/mk_theater.cfg', json.dumps(self.mk_config), True)
        else:
            pass
        reactor.connectSSL(self.mk_config['MediaKrakenServer']['Host'],
            int(self.mk_config['MediaKrakenServer']['Port']),
            MKFactory(), ssl.ClientContextFactory())

    def send_twisted_message_thread(self, message):
        MKFactory.protocol.sendline_data(twisted_connection, message)

    def process_message(self, server_msg):
        """
        Process network message from server
        """
        json_message = json.loads(server_msg)
        try:
            if json_message['Type'] != "Image":
                logging.info("Got Message: %s", server_msg)
            else:
                logging.info("Got Image Message: %s %s", json_message['Sub'], json_message['UUID'])
        except:
            logging.info("full record: %s", server_msg)
        logging.info("len total: %s", len(server_msg))
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident', 'UUID': str(uuid.uuid4()),
                'Platform': platform.node()}))
            # start up the image refresh since we have a connection
            # TODO this is kivy code - Clock.schedule_interval(self.main_image_refresh, 5.0)
        elif json_message['Type'] == "Media":
            if json_message['Sub'] == "Detail":
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_Detail'
                self.root.ids.theater_media_video_title.text = json_message['Data']['Meta']['themoviedb']['Meta']['title']
                self.root.ids.theater_media_video_subtitle.text = json_message['Data']['Meta']['themoviedb']['Meta']['tagline']
                # self.root.ids.theater_media_video_rating = row_data[3]['']
                self.root.ids.theater_media_video_runtime.text = str(json_message['Data']['Meta']['themoviedb']['Meta']['runtime'])
                self.root.ids.theater_media_video_overview.text = json_message['Data']['Meta']['themoviedb']['Meta']['overview']
                genres_list = ''
                for ndx in range(0, len(json_message['Data']['Meta']['themoviedb']['Meta']['genres'])):
                    genres_list += (json_message['Data']['Meta']['themoviedb']['Meta']['genres'][ndx]['name'] + ', ')
                self.root.ids.theater_media_video_genres.text = genres_list[:-2]
                # "LocalImages": {"Banner": "", "Fanart": "",
                # "Poster": "../images/poster/f/9mhyID0imBjaRj3FJkARuXXSiQU.jpg", "Backdrop": null},
                production_list = ''
                for ndx in range(0, len(json_message['Data']['Meta']['themoviedb']['Meta']['production_companies'])):
                    production_list += (json_message['Data']['Meta']['themoviedb']['Meta']['production_companies'][ndx]['name'] + ', ')
                self.root.ids.theater_media_video_production_companies.text = production_list[:-2]
                # go through streams
                audio_streams = []
                subtitle_streams = ['None']
                if json_message['Data2'] is not None and 'FFprobe' in json_message['Data2'] \
                        and 'streams' in json_message['Data2']['FFprobe']\
                        and json_message['Data2']['FFprobe']['streams'] is not None:
                    for stream_info in json_message['Data2']['FFprobe']['streams']:
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
                data = [{'text': str(i), 'is_selected': False} for i in range(100)]
                args_converter = lambda row_index,\
                                        rec: {'text': rec['text'], 'size_hint_y': None, 'height': 25}
                list_adapter = ListAdapter(data=data, args_converter=args_converter,
                                           cls=ListItemButton, selection_mode='single', allow_empty_selection=False)
                list_view = ListView(adapter=list_adapter)
                for video_list in json_message['Data']:
                    logging.info('vid list item %s', video_list)
                    btn1 = ToggleButton(text=video_list[0], group='button_group_video_list',
                                        size_hint_y=None,
                                        width=self.root.ids.theater_media_video_list_scrollview.width,
                                        height=(self.root.ids.theater_media_video_list_scrollview.height / 8))
                    btn1.bind(on_press=partial(self.theater_event_button_video_select, video_list[1]))
                    self.root.ids.theater_media_video_list_scrollview.add_widget(btn1)
        elif json_message['Type'] == 'Play': # direct file play
            # AttributeError: 'NoneType' object has no attribute
            # 'set_volume'  <- means can't find file
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
            video_source_dir = json_message['Data']
            share_mapping = (('/mediakraken/mnt/zfsspoo/', '/home/spoot/zfsspoo/'),)
            if share_mapping is not None:
                for mapping in share_mapping.iteritems():
                    video_source_dir = video_source_dir.replace(mapping[0], mapping[1])
            self.root.ids.theater_media_video_videoplayer.source = video_source_dir
            self.root.ids.theater_media_video_videoplayer.volume = 1
            self.root.ids.theater_media_video_videoplayer.state = 'play'
        # after connection receive the list of users to possibly login with
        elif json_message['Type'] == "User":
            pass

        elif json_message['Type'] == "Genre List":
            logging.info("gen")
            for genre_list in json_message:
                logging.info("genlist: %s", genre_list)
                btn1 = ToggleButton(text=genre_list[0], group='button_group_genre_list',
                                    size_hint_y=None,
                                    width=self.root.ids.theater_media_genre_list_scrollview.width,
                                    height=(self.root.ids.theater_media_genre_list_scrollview.height / 8))
                btn1.bind(on_press=partial(self.Theater_Event_Button_Genre_Select, genre_list[0]))
                self.root.ids.theater_media_genre_list_scrollview.add_widget(btn1)

        elif json_message['Type'] == "Image":
            if json_message['Sub'] == "Movie":
                logging.info("here for movie refresh")
                if json_message['Sub2'] == "Demo":
                    self.home_demo_file_name = str(uuid.uuid4())
                    f = open(self.home_demo_file_name, "w")
                    f.write(base64.b64decode(json_message['Data']))
                    f.close()
                    self.demo_media_id = json_message['UUID']
                    proxy_image_demo = Loader.image(self.home_demo_file_name)
                    proxy_image_demo.bind(on_load=self._image_loaded_home_demo)
                    pass
                elif json_message['Sub2'] == "Movie":
                    # texture = Texture.create(size=(640, 480), colorfmt=str('rgba'))
                    # texture.blit_buffer(base64.b64decode(json_message['Data']))
                    # self.root.ids.main_home_movie_image.texture = Image(size=texture.size, texture=texture).texture
                    #self.root.ids.main_home_movie_image.texture = ImageLoaderPygame(StringIO.StringIO(base64.b64decode(json_message['Data']))).texture
                    self.home_movie_file_name = str(uuid.uuid4())
                    f = open(self.home_movie_file_name, "w")
                    f.write(base64.b64decode(json_message['Data']))
                    f.close()
                    proxy_image_movie = Loader.image(self.home_movie_file_name)
                    proxy_image_movie.bind(on_load=self._image_loaded_home_movie)
                elif json_message['Sub2'] == "New Movie":
                    self.home_movie_new_file_name = str(uuid.uuid4())
                    f = open(self.home_movie_new_file_name, "w")
                    f.write(base64.b64decode(json_message['Data']))
                    f.close()
                    proxy_image_new_movie = Loader.image(self.home_movie_new_file_name)
                    proxy_image_new_movie.bind(on_load=self._image_loaded_home_new_movie)
                elif json_message['Sub2'] == "In Progress":
                    self.home_movie_inprogress_file_name = str(uuid.uuid4())
                    f = open(self.home_movie_inprogress_file_name, "w")
                    f.write(base64.b64decode(json_message['Data']))
                    f.close()
                    proxy_image_prog_movie = Loader.image(self.home_movie_inprogress_file_name)
                    proxy_image_prog_movie.bind(on_load=self._image_loaded_home_prog_movie)
            # elif pickle_data[0] == "MOVIEDETAIL":
            #     logging.info("here for movie detail refresh: %s", pickle_data[1])
            #     proxy_image_detail_movie = Loader.image(pickle_data[1])
            #     proxy_image_detail_movie.bind(on_load=self._image_loaded_detail_movie)
        else:
            logging.error("unknown message type")

    def main_button_books_clicked(self):
        pass

    def main_button_home_movie_clicked(self):
        pass

    def main_button_images_clicked(self):
        pass

    def main_button_movie_clicked(self):
        self.window_browse_movie.show()

    def main_button_music_clicked(self):
        pass

    def main_button_radio_clicked(self):
        pass

    def main_button_settings_clicked(self):
        pass

    def main_button_tv_clicked(self):
        pass

    def main_button_tv_live_clicked(self):
        pass


if __name__ == '__main__':
    # for windows exe support
    from multiprocessing import freeze_support
    freeze_support()
    # begin logging
    common_logging.com_logging_start('./log/MediaKraken_Theater_QT')
    # finish app setup
    app = QApplication(sys.argv)
    import qt5reactor
    qt5reactor.install()
    # has to be after the install of qt5reactor
    from twisted.internet import reactor
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
