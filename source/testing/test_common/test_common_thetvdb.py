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

sys.path.append('.')
from common import common_config_ini
from common import common_thetvdb


class TestCommonTheTVDB:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.thetvdb_connection = common_thetvdb.CommonTheTVDB(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # get show information
#    def com_TheTVDB_Show_Info(self, show_title, show_language):


# search for show
#    def com_TheTVDB_Search(self, show_title, show_year, show_id, show_language, save_db=True):


# save entire show info
#    def com_TheTVDB_Show_DB_Save(self, show_data):


# get episode information
#    def com_TheTVDB_Episode_Info(self, show_language, episode_id):


# get episode information by season and episode
#    def com_TheTVDB_Season_Episode_Info(self, show_language, season_no, ep_no, show_id):


# show data from result
#    def com_TheTVDB_Show_Details(self, show_data):
