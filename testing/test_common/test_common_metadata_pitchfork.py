'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import pytest
import sys
sys.path.append("../common")
from com_meta_pitchfork import *


class TestCommonpitchfork(object):


    @classmethod
    def setup_class(self):
        self.db_connection.connection = com_pitchfork_API()


    @classmethod
    def teardown_class(self):
        pass


    @pytest.mark.parametrize(("artist_name", "album_title"), [
        ("Megadeath", "Youthanasia"),
        ("FakeBand", "FakeAlbum")])
    def test_com_pitchfork_Search(self, artist_name, album_title):
        self.db_connection.com_pitchfork_Search(artist_name, album_title)


    def test_com_pitchfork_Album_Title(self):
        self.db_connection.com_pitchfork_Album_Title()


    def test_com_pitchfork_Album_Label(self):
        self.db_connection.com_pitchfork_Album_Label()


    def test_com_pitchfork_Album_Review(self):
        self.db_connection.com_pitchfork_Album_Review()


    def test_com_pitchfork_Album_Cover_Art_Link(self):
        self.db_connection.com_pitchfork_Album_Cover_Art_Link()


    def test_com_pitchfork_Album_Review_Score(self):
        self.db_connection.com_pitchfork_Album_Review_Score()
