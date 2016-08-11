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
from MK_Common_Metadata_TVMaze import *


class Test_MK_Common_Metadata_TVMaze_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Metadata_TVMaze_API()


    @classmethod
    def teardown_class(self):
        pass


# show list 50 per page - 0 is first page
# def MK_Common_Metadata_TheMaze_Show_List(self, page_no=0):


    # show when last updated
    def test_MK_Common_Metadata_TheMaze_Show_Updated(self):
        self.db.MK_Common_Metadata_TheMaze_Show_Updated()


# lookup show
# def MK_Common_Metadata_TheMaze_WideSearch(self, show_name, show_year=None):


# lookup specific show
# def MK_Common_Metadata_TheMaze_NarrowSearch(self, show_name, show_year=None):


# lookup specific id
# def MK_Common_Metadata_TheMaze_Show_By_ID(self, tvmaze_id, tvrage_id, imdb_id, tvdb_id, embed_info=True):


# people search (doesnt' appear to have episode data here)
# def MK_Common_Metadata_TheMaze_Person_By_Name(self, person_name):


# schedule
# def MK_Common_Metadata_TheMaze_Schedule(self, country_code=None, schedule_date=None):
