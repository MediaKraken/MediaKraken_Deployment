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
sys.path.append('.')
from common import common_metadata_gamesdb


class TestCommonMetadataGamesDB(object):


    @classmethod
    def setup_class(self):
        self.gamesdb_connection = common_metadata_gamesdb.CommonMetadataGamesDB()


    @classmethod
    def teardown_class(self):
        pass


    def test_com_meta_gamesdb_platform_list(self):
        """
        Test function
        """
        self.gamesdb_connection.com_meta_gamesdb_platform_list()


# def com_meta_gamesdb_Platform_by_ID(self, platform_id):


    # 'mega man' as mega OR man
    def test_com_meta_gamesdb_games_by_name_or(self):
        """
        Test function
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_name_or("Mega Man")


    # 'mega man' as mega AND man
    def test_com_meta_gamesdb_games_by_name_and(self):
        """
        Test function
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_name_and("Mega Man")


# def com_meta_gamesdb_Games_by_Name_And_Platform_Or(self, game_name, platform_name, game_genre=None):


# def com_meta_gamesdb_Games_by_Name_And_Platform_And(self, game_name, platform_name, game_genre=None):


# def com_meta_gamesdb_Games_by_Platform_ID(self, platform_id):


# def com_meta_gamesdb_Games_by_ID(self, game_id):
