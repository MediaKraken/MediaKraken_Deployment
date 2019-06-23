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

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_metadata_thegamesdb


class TestCommonMetadataGamesDB:

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

    @pytest.mark.parametrize(("platform_id"), [
        ("1"),
        ("9038489378934789548903478923")])
    def test_com_meta_gamesdb_platform_by_id(self, platform_id):
        """
        Platform info by id
        """
        self.gamesdb_connection.com_meta_gamesdb_platform_by_id(platform_id)

    @pytest.mark.parametrize(("game_name"), [
        ("Halo"),
        ("Zjfwoij03478923")])
    def test_com_meta_gamesdb_games_by_name(self, game_name):
        """
        # 'mega man'
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_name(game_name)

    @pytest.mark.parametrize(("game_id"), [
        ("1"),
        ("23425363452442354654")])
    def test_com_meta_gamesdb_games_by_id(self, game_id):
        """
        # game by id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_id(game_id)

    @pytest.mark.parametrize(("game_id"), [
        ("1"),
        ("23425363452442354654")])
    def test_com_meta_gamesdb_games_art_by_id(self, game_id):
        """
        # game by id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_art_by_id(game_id)

    @pytest.mark.parametrize(("platform_id"), [
        ("1"),
        ("9038489378934789548903478923")])
    def test_com_meta_gamesdb_games_by_platform_id(self, platform_id):
        """
        Games by platform id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_platform_id(
            platform_id)

    @pytest.mark.parametrize(("platform_name"), [
        ("SNES"),
        ("Fakehtignsio")])
    def test_com_meta_gamesdb_games_by_platform_name(self, platform_name):
        """
        Games by platform id
        """
        self.gamesdb_connection.com_meta_gamesdb_games_by_platform_name(
            platform_name)

    @pytest.mark.parametrize(("update_time"), [
        ("234553")])
    def test_com_meta_gamesdb_games_updated_seconds(self, update_time):
        """
        Games updated in last n seconds
        """
        self.gamesdb_connection.com_meta_gamesdb_games_updated_seconds(
            update_time)
