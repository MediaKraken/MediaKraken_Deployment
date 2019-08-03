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
import database as database_base


class TestDatabaseMetadataMusicVideo:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # query to see if song is in local DB
    # def db_meta_music_video_lookup(self, artist_name, song_title):
    #         self.db_connection.db_rollback()

    # def db_meta_music_video_add(self, artist_name, artist_song, id_json, data_json, image_json):
    #         self.db_connection.db_rollback()

    # def db_meta_music_video_detail_uuid(self, item_guid):
    #         self.db_connection.db_rollback()

    # def db_meta_music_video_count(self, imvdb_ID=None):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_music_video_list(self, offset, records):
        """
        Music list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_music_video_list(offset, records)
