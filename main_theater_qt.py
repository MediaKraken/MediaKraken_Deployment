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
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QDialog, QApplication
sys.path.append('theater_qt')
from common import common_version
from ui import mk_browse_movie_ui
from ui import mk_login_ui
from ui import mk_mainwindow_ui
from ui import mk_player_ui


class BrowseMovieWindow(QMainWindow, mk_browse_movie_ui.Ui_MK_Browse_Movie):
    def __init__(self, parent=None):
        super(BrowseMovieWindow, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow, mk_mainwindow_ui.Ui_MK_MainWindow):
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
        # setup the other windows (this way only done once to negate memory leak
        self.window_browse_movie = BrowseMovieWindow(self)

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
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
