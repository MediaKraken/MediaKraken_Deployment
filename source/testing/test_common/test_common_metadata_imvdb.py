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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_config_ini
from common import common_metadata_imvdb


class TestCommonimvdb:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.imvdb_connection = common_metadata_imvdb.CommonMetadataIMVdb(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # def com_imvdb_Video_Info(self, video_id):

    @pytest.mark.parametrize(("artist_name", "song_title"), [
        ('Megadeath', 'Trust'),
        ('Garbage', 'Empty'),
        ('fake', 'fake')])
    def test_com_imvdb_search_video(self, artist_name, song_title):
        """
        Test function
        """
        self.imvdb_connection.com_imvdb_search_video(artist_name, song_title)

    @pytest.mark.parametrize(("artist_name"), [
        ('Megadeath'),
        ('Garbage'),
        ('fake')])
    def test_com_imvdb_search_entities(self, artist_name):
        """
        Test function
        """
        self.imvdb_connection.com_imvdb_search_entities(artist_name)
