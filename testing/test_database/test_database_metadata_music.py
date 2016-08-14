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


class TestDatabaseMetadataMusic(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # query to see if song is in local DB
    # def srv_db_music_lookup(self, artist_name, album_name, song_title):
#         self.db_connection.srv_db_rollback()


    # return musician data by guid
    # def srv_db_meta_musician_by_guid(self, guid):
#         self.db_connection.srv_db_rollback()


    # insert musician
    # def srv_db_meta_musician_add(self, data_name, data_id, data_json):
#         self.db_connection.srv_db_rollback()


    # return album data by guid
    # def srv_db_meta_album_by_guid(self, guid):
#         self.db_connection.srv_db_rollback()


    # insert album
    # def srv_db_meta_album_add(self, data_name, data_id, data_json):
#        self.db_connection.srv_db_rollback()


    # return song data by guid
    # def srv_db_meta_song_by_guid(self, guid):
#        self.db_connection.srv_db_rollback()


    # insert song
    # def srv_db_meta_song_add(self, data_name, data_id, data_json):
#        self.db_connection.srv_db_rollback()


    # return song list from ablum guid
    # def srv_db_meta_songs_by_album_guid(self, guid):
#        self.db_connection.srv_db_rollback()


    # return albums metadatalist
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_meta_album_list(self, offset, records):
        self.db_connection.srv_db_meta_album_list(offset, records)
        self.db_connection.srv_db_rollback()


    # return muscian metadatalist
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_meta_muscian_list(self, offset, records):
        self.db_connection.srv_db_meta_muscian_list(offset, records)
        self.db_connection.srv_db_rollback()
