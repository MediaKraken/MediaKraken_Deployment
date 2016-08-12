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


class Test_database_metadata_music:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # query to see if song is in local DB
    # def MK_Server_Database_Music_Lookup(self, artist_name, album_name, song_title):
#         self.db.MK_Server_Database_Rollback()


    # return musician data by guid
    # def MK_Server_Database_Metadata_Musician_By_GUID(self, guid):
#         self.db.MK_Server_Database_Rollback()


    # insert musician
    # def MK_Server_Database_Metadata_Musician_Add(self, data_name, data_id, data_json):
#         self.db.MK_Server_Database_Rollback()


    # return album data by guid
    # def MK_Server_Database_Metadata_Album_By_GUID(self, guid):
#         self.db.MK_Server_Database_Rollback()


    # insert album
    # def MK_Server_Database_Metadata_Album_Add(self, data_name, data_id, data_json):
#        self.db.MK_Server_Database_Rollback()


    # return song data by guid
    # def MK_Server_Database_Metadata_Song_By_GUID(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # insert song
    # def MK_Server_Database_Metadata_Song_Add(self, data_name, data_id, data_json):
#        self.db.MK_Server_Database_Rollback()


    # return song list from ablum guid
    # def MK_Server_Database_Metadata_Songs_By_Album_GUID(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # return albums metadatalist
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Metadata_Album_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Album_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # return muscian metadatalist
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Metadata_Muscian_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Muscian_List(offset, records)
        self.db.MK_Server_Database_Rollback()
