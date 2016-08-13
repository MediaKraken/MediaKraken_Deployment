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
from com_db_emby import *


class TestCommonDatabaseEmby(object):


    @classmethod
    def setup_class(self):
        self.db = com_db_Attach_Emby(None):


    @classmethod
    def teardown_class(self):
        self.db.com_db_Close_Emby()



# open database and pull in config from sqlite and create db if not exist
#def com_db_Open_Emby(db_file_name = None, db_username_dir = os.environ.get("USERNAME"), 


    # grab all movies in emby database
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def Test_com_db_Movie_List_Emby(self, offset, records):
        self.db.com_db_Movie_List_Emby(offset, records)


    # grab all movies in emby database count
    def teset_com_db_Movie_List_Emby_Count(self):
        self.db.com_db_Movie_List_Emby_Count()


    # grab all the tv episodes in the emby database
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def com_db_TV_List_Emby(self, offset, records):
        self.db.com_db_TV_List_Emby(offset, records)


    # grab all the tv episodes in the emby database count
    def Test_com_db_TV_List_Emby_Count(self):
        self.db.com_db_TV_List_Emby_Count()


    # grab all the tv episodes and movies in the emby database
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def Test_com_db_TV_Movie_List_Emby(self, offset, records):
        self.db.com_db_TV_Movie_List_Emby(offset, records)


    # grab all the tv episodes and movies in the emby database count
    def Test_com_db_TV_Movie_List_Emby_Count(self):
        self.db.com_db_TV_Movie_List_Emby_Count()


# grab all users from database
#def com_db_Users_List(offset=None, records=None, play_stats = None):


    # grab count of all users
    def Test_com_db_Users_List_Count(self):
        self.db.com_db_Users_List_Count()


# grab last IP
#def com_db_User_Last_IP(user_id):


# get all the media files that match directory
#def com_db_Media_In_Dir(dir_name):


    # grab all activity data
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def com_db_Emby_Activity_List(self, offset, records):
        self.db.com_db_Emby_Activity_List(offset, records)


    # grab all activity data count
    def Test_com_db_Emby_Activity_List_Count(self):
        self.db.com_db_Emby_Activity_List_Count()


    # grab all notifications
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def Test_MK_Databas_Sqlite3_Emby_Notification_List(self, offset, records):
        self.db.MK_Databas_Sqlite3_Emby_Notification_List(offset, records)


    # grab notification  data count
    def Test_com_db_Emby_Notification_List_Count(self):
        self.db.com_db_Emby_Notification_List_Count()


    # grab all notifications
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def Test_com_db_Emby_Sync_List(self, offset, records):
        self.db.com_db_Emby_Sync_List(offset, records):


    # grab notification  data count
    def Test_com_db_Emby_Sync_List_Count(self):
        self.db.com_db_Emby_Sync_List_Count()


# get id to lookup from metadata
#def com_db_Media_By_Guid(guid):


    # all data from users for playback
    def Test_com_db_User_Play_Data(self):
        self.db.com_db_User_Play_Data()
