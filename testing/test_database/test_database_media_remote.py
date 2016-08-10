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
sys.path.append("../common")
sys.path.append("../server") # for db import
import database as database_base


class Test_database_media_remote:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # insert media into database
    # def MK_Server_Database_Insert_Remote_Media(self, media_link_uuid, media_uuid, media_class_uuid, media_metadata_uuid, media_ffprobe_json):
#        self.db.MK_Server_Database_Rollback()


    # read in all media unless guid specified
    # def MK_Server_Database_Read_Remote_Media(self, media_guid=None):
#        self.db.MK_Server_Database_Rollback()


    # count known media
    def test_MK_Server_Database_Known_Remote_Media_Count(self):
        self.db.MK_Server_Database_Known_Remote_Media_Count()
        self.db.MK_Server_Database_Rollback()


    # processed via main_link........
    ## process new records from network sync event from linked server
    #def MK_Server_Database_Media_Remote_New_Data(self, link_uuid, link_records):
#        self.db.MK_Server_Database_Rollback()


    # new media for link
    # def MK_Server_Database_Media_Remote_Read_New(self, date_last_sync, sync_movie=None, sync_tv=None, sync_sports=None, sync_music=None, sync_music_video=None, sync_book=None):
#        self.db.MK_Server_Database_Rollback()
