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
import database as database_base


class TestDatabaseMetadataGames:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # return game system data
    # def db_meta_game_system_by_guid(self, guid):
    #        self.db_connection.db_rollback()

    def test_db_meta_game_system_list_count(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_game_system_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_game_system_list(self, offset, records):
        """
        # return list of game systems
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_game_system_list(offset, records)

    def test_db_meta_game_list_count(self):
        """
        # return list of games count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_game_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_game_list(self, offset, records):
        """
        # return list of games
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_game_list(offset, records)

    # return game data
    # def db_meta_game_by_guid(self, guid):
#        self.db_connection.db_rollback()


# game list by system count
# def db_meta_game_by_system_count(self, guid):
#        self.db_connection.db_rollback()


# game list by system count
# def db_meta_game_by_system(self, guid, offset=None, records=None):
#        self.db_connection.db_rollback()


# game by sha1
# def db_meta_game_by_sha1(self, sha1_hash):
#        self.db_connection.db_rollback()


# game by name and system short name
# def db_meta_game_by_name_and_system(self, game_name, game_system_short_name):
#        self.db_connection.db_rollback()
