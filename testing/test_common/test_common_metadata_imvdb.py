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
from com_Metadata_IMVDb import *


class TestCommonIMVDb(object):


    @classmethod
    def setup_class(self):
        self.db = com_Metadata_IMVDb.com_IMVDb_API()


    @classmethod
    def teardown_class(self):
        pass


# def com_IMVDb_Video_Info(self, video_id):


    @pytest.mark.parametrize(("artist_name", "song_title"), [
        ('Megadeath', 'Trust'),
        ('Garbage', 'Empty'),
        ('fake', 'fake')])
    def Test_com_IMVDb_Search_Video(self, artist_name, song_title):
        com_IMVDb_Search_Video(artist_name, song_title)


    @pytest.mark.parametrize(("artist_name"), [
        ('Megadeath'),
        ('Garbage'),
        ('fake')])
    def Test_com_IMVDb_Search_Entities(self, artist_name):
        com_IMVDb_Search_Entities(artist_name)
