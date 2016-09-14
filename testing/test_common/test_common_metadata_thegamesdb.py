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
from common import common_metadata_thegamesdb


class TestCommonMetadataGamesDB(object):


    @classmethod
    def setup_class(self):
        self.gamesdb_connection = common_metadata_thegamesdb.CommonMetadataGamesDB()


    @classmethod
    def teardown_class(self):
        pass


    def test_com_meta_gamesdb_platform_list(self):
        """
        Test function
        """
        self.gamesdb_connection.com_meta_gamesdb_platform_list()


    def test_com_meta_gamesdb_platform_by_id(self, platform_id):
        """
        Platform info by id
        """
        self.gamesdb_connection.com_meta_gamesdb_platform_by_id(self, platform_id)


    def test_com_meta_gamesdb_games_by_name(self, game_name):
        """
        # 'mega man'
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_name(self, game_name)


    def test_com_meta_gamesdb_games_by_id(self, game_id):
        """
        # game by id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_id(self, game_id)


    def test_com_meta_gamesdb_games_art_by_id(self, game_id):
        """
        # game by id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_art_by_id(self, game_id)


    def test_com_meta_gamesdb_games_by_platform_id(self, platform_id):
        """
        Games by platform id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_platform_id(self, platform_id)


    def test_com_meta_gamesdb_games_by_platform_name(self, platform_name):
        """
        Games by platform id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_platform_name(self, platform_name)


    def test_com_meta_gamesdb_games_updated_seconds(self, update_time):
        """
        Games updated in last n seconds
        """
        self.gamesdb_connection.com_meta_gamesdb_games_updated_seconds(self, update_time)
