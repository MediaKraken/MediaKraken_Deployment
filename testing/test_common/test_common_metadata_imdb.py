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
from common_metadata_imdb import *


class TestCommonimdb(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_metadata_imdb.com_imdb_API()


    @classmethod
    def teardown_class(self):
        pass


    # fetch info from title
    def test_com_imdb_Title_Search(self):
        com_imdb_Title_Search("Robocop")


# fetch info by ttid
# def com_imdb_ID_Search(self, media_id):


# fetch person info by id
# def com_imdb_Person_by_ID(self, person_id):


# fetch person images by id
# def com_imdb_Person_Images_by_Id(self, person_id):


# fetch the title review
# def com_imdb_Title_Review_by_ID(self, media_id):
