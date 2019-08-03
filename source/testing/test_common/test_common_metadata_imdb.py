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
from common import common_metadata_imdb


class TestCommonimdb:

    @classmethod
    def setup_class(self):
        self.imdb_connection = common_metadata_imdb.CommonMetadataIMDB()

    @classmethod
    def teardown_class(self):
        pass

    # fetch info from title
    def test_com_imdb_title_search(self):
        """
        Test function
        """
        self.imdb_connection.com_imdb_title_search("Robocop")

    # fetch info by ttid
    # def com_imdb_ID_Search(self, media_id):

    # fetch person info by id
    # def com_imdb_Person_by_ID(self, person_id):

    # fetch person images by id
    # def com_imdb_Person_Images_by_Id(self, person_id):

    # fetch the title review
    # def com_imdb_Title_Review_by_ID(self, media_id):
