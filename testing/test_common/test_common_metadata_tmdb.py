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
sys.path.append("./common")
import common_metadata_tmdb


class TestCommonMetadataTMDB(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_metadata_tmdb.com_metadata_tmdb_API()


    @classmethod
    def teardown_class(self):
        pass


# search for movie title and year
# def com_tmdb_Search(self, movie_title, movie_year=None, id_only=False):


# search by tmdb
# def com_tmdb_Metadata_by_ID(self, tmdb_id):


# search by tmdb
# def com_tmdb_Metadata_Cast_by_ID(self, tmdb_id):


# review by tmdb
# def com_tmdb_Metadata_Review_by_ID(self, tmdb_id):


    # movie changes since date within 24 hours
    def test_com_tmdb_Metadata_Changes_Movie(self):
        com_tmdb_Metadata_Changes_Movie()


    # tv changes since date within 24 hours
    def test_com_tmdb_Metadata_Changes_TV(self):
        com_tmdb_Metadata_Changes_TV()


    # person changes since date within 24 hours
    def test_com_tmdb_Metadata_Changes_Person(self):
        com_tmdb_Metadata_Changes_Person()


# collection info
# def com_tmdb_Metadata_Collection_by_ID(self, tmdb_id):


# download info and set data to be ready for insert into database
# def com_tmdb_MetaData_Info_Build(self, result_json):
