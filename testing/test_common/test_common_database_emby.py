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
import pytest # pylint: disable=W0611
import sys
sys.path.append('.')
from common import common_database_emby


class TestCommonDatabaseEmby(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_database_emby.CommonDatabaseEmby()
        self.db_connection.com_db_open_emby(None)


    @classmethod
    def teardown_class(self):
        self.db_connection.com_db_close_emby()



# open database and pull in config from sqlite and create db if not exist
#def com_db_Open_Emby(db_file_name = None, db_username_dir = os.environ.get("USERNAME"), 


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_movie_list_emby(self, offset, records):
        """
        # grab all movies in emby database
        """
        self.db_connection.com_db_movie_list_emby(offset, records)


    def test_com_db_movie_list_emby_count(self):
        """
        # grab all movies in emby database count
        """
        self.db_connection.com_db_movie_list_emby_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_tv_list_emby(self, offset, records):
        """
        # grab all the tv episodes in the emby database
        """
        self.db_connection.com_db_tv_list_emby(offset, records)


    def test_com_db_tv_list_emby_count(self):
        """
        # grab all the tv episodes in the emby database count
        """
        self.db_connection.com_db_tv_list_emby_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_tv_movie_list_emby(self, offset, records):
        """
        # grab all the tv episodes and movies in the emby database
        """
        self.db_connection.com_db_tv_movie_list_emby(offset, records)


    def test_com_db_tv_movie_list_emby_count(self):
        """
        # grab all the tv episodes and movies in the emby database count
        """
        self.db_connection.com_db_tv_movie_list_emby_count()


# grab all users from database
#def com_db_Users_List(offset=None, records=None, play_stats = None):


    def test_com_db_users_list_count(self):
        """
        # grab count of all users
        """
        self.db_connection.com_db_users_list_count()


# grab last IP
#def com_db_User_Last_IP(user_id):


# get all the media files that match directory
#def com_db_Media_In_Dir(dir_name):


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_emby_activity_list(self, offset, records):
        """
        # grab all activity data
        """
        self.db_connection.com_db_emby_activity_list(offset, records)


    def test_com_db_emby_activity_list_count(self):
        """
        # grab all activity data count
        """
        self.db_connection.com_db_emby_activity_list_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_emby_notification_list(self, offset, records):
        """
        # grab all notifications
        """
        self.db_connection.test_com_db_emby_notification_list(offset, records)


    def test_com_db_emby_notice_list_count(self):
        """
        # grab notification data count
        """
        self.db_connection.com_db_emby_notice_list_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_com_db_emby_sync_list(self, offset, records):
        """
        # grab all sync
        """
        self.db_connection.com_db_emby_sync_list(offset, records)


    def test_com_db_emby_sync_list_count(self):
        """
        # grab notification  data count
        """
        self.db_connection.com_db_emby_sync_list_count()


# get id to lookup from metadata
#def com_db_Media_by_Guid(guid):


    def test_com_db_user_play_data(self):
        """
        # all data from users for playback
        """
        self.db_connection.com_db_user_play_data()
