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
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class TestDatabaseMetadataMusicVideo(object):


    @classmethod
    def setup_class(self):
        self.db_connection.connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # query to see if song is in local DB
    # def srv_db_meta_music_video_lookup(self, artist_name, song_title):
#         self.db_connection.srv_db_rollback()


    # def srv_db_meta_music_video_add(self, artist_name, artist_song, id_json, data_json, image_json):
#         self.db_connection.srv_db_rollback()


    # def srv_db_meta_music_video_detail_by_uuid(self, item_guid):
#         self.db_connection.srv_db_rollback()


    # def srv_db_meta_music_video_count(self, imvdb_ID=None):
#        self.db_connection.srv_db_rollback()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_meta_music_video_list(self, offset, records):
        self.db_connection.srv_db_meta_music_video_list(offset, records)
        self.db_connection.srv_db_rollback()
