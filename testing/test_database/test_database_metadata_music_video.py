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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")  # for db import
import database as database_base


class Test_database_metadata_music_video:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # query to see if song is in local DB
    # def MK_Server_Database_Metadata_Music_Video_Lookup(self, artist_name, song_title):
#         self.db.MK_Server_Database_Rollback()


    # def MK_Server_Database_Metadata_Music_Video_Add(self, artist_name, artist_song, id_json, data_json, image_json):
#         self.db.MK_Server_Database_Rollback()


    # def MK_Server_Database_Metadata_Music_Video_Detail_By_UUID(self, item_guid):
#         self.db.MK_Server_Database_Rollback()


    # def MK_Server_Database_Metadata_Music_Video_Count(self, IMVDb_ID=None):
#        self.db.MK_Server_Database_Rollback()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_MK_Server_Database_Metadata_Music_Video_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Music_Video_List(offset, records)
        self.db.MK_Server_Database_Rollback()
