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
from common_meta_gamesdb import *


class TestCommonMetadataGamesDB(object):


    @classmethod
    def setup_class(self):
        self.gamesdb_connection = com_meta_GamesDB.com_meta_GamesDB_API()


    @classmethod
    def teardown_class(self):
        pass


    def test_com_meta_GamesDB_Platform_List(self):
        com_meta_GamesDB_Platform_List()


# def com_meta_GamesDB_Platform_by_ID(self, platform_id):


    # 'mega man' as mega OR man
    def test_com_meta_GamesDB_Games_by_Name_Or(self):
        com_meta_GamesDB_Games_by_Name_Or("Mega Man")


    # 'mega man' as mega AND man
    def test_com_meta_GamesDB_Games_by_Name_And(self):
        com_meta_GamesDB_Games_by_Name_And("Mega Man")


# def com_meta_GamesDB_Games_by_Name_And_Platform_Or(self, game_name, platform_name, game_genre=None):


# def com_meta_GamesDB_Games_by_Name_And_Platform_And(self, game_name, platform_name, game_genre=None):


# def com_meta_GamesDB_Games_by_Platform_ID(self, platform_id):


# def com_meta_GamesDB_Games_by_ID(self, game_id):
