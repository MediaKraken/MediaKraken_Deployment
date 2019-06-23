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
from common import common_metadata_tvmaze


class TestCommonMetadatatvmaze:

    @classmethod
    def setup_class(self):
        self.db_connection = common_metadata_tvmaze.CommonMetadatatvmaze()

    @classmethod
    def teardown_class(self):
        pass

    # show list 50 per page - 0 is first page
    # def com_meta_TheMaze_Show_List(self, page_no=0):

    # show when last updated
    def test_com_meta_tvmaze_show_updated(self):
        """
        Test function
        """
        self.db_connection.com_meta_tvmaze_show_updated()

    # lookup show
    # def com_meta_TvMaze_WideSearch(self, show_name, show_year=None):

    # lookup specific show
    # def com_meta_TvMaze_NarrowSearch(self, show_name, show_year=None):

    # lookup specific id
    # def com_meta_TvMaze_Show_by_ID(self, tvmaze_id, imdb_id, tvdb_id, embed_info=True):

    # people search (doesnt' appear to have episode data here)
    # def com_meta_TvMaze_Person_by_Name(self, person_name):

    # schedule
    # def com_meta_TvMaze_Schedule(self, country_code=None, schedule_date=None):
