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
from common_metadata_tmdb import *


class test_common_metadata_tmdb_API:


    @classmethod
    def setup_class(self):
        self.db = common_metadata_tmdb.common_metadata_tmdb_API()


    @classmethod
    def teardown_class(self):
        pass


# search for movie title and year
# def MK_Common_TMDB_Search(self, movie_title, movie_year=None, id_only=False):


# search by tmdb
# def MK_Common_TMDB_Metadata_By_ID(self, tmdb_id):


# search by tmdb
# def MK_Common_TMDB_Metadata_Cast_By_ID(self, tmdb_id):


# review by tmdb
# def MK_Common_TMDB_Metadata_Review_By_ID(self, tmdb_id):


    # movie changes since date within 24 hours
    def test_MK_Common_TMDB_Metadata_Changes_Movie(self):
        MK_Common_TMDB_Metadata_Changes_Movie()


    # tv changes since date within 24 hours
    def test_MK_Common_TMDB_Metadata_Changes_TV(self):
        MK_Common_TMDB_Metadata_Changes_TV()


    # person changes since date within 24 hours
    def test_MK_Common_TMDB_Metadata_Changes_Person(self):
        MK_Common_TMDB_Metadata_Changes_Person()


# collection info
# def MK_Common_TMDB_Metadata_Collection_By_ID(self, tmdb_id):


# download info and set data to be ready for insert into database
# def MK_Common_TMDB_MetaData_Info_Build(self, result_json):
