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
from MK_Common_TheTVDB import *


class Test_MK_Common_TheTVDB_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_TheTVDB.MK_Common_TheTVDB_API()


    @classmethod
    def teardown_class(self):
        pass


    # get show information
#    def MK_Common_TheTVDB_Show_Info(self, show_title, show_language):


    # search for show
#    def MK_Common_TheTVDB_Search(self, show_title, show_year, show_id, show_language, save_db=True):


    # save entire show info
#    def MK_Common_TheTVDB_Show_DB_Save(self, show_data):


    # get episode information
#    def MK_Common_TheTVDB_Episode_Info(self, show_language, episode_id):


    # get episode information by season and episode
#    def MK_Common_TheTVDB_Season_Episode_Info(self, show_language, season_no, ep_no, show_id):


    # show data from result
#    def MK_Common_TheTVDB_Show_Details(self, show_data):
