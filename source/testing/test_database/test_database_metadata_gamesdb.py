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

import json
import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseMetadataGamesdb:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("platform_id", "platform_name", "platform_alias", "platform_json"), [
        (34, 'Test', 'Test', json.dumps({'Tt': 'M'})),
        (3, 'Tst', 'Tst', None)])
    def test_db_meta_gamesdb_system_insert(self, platform_id, platform_name,
                                           platform_alias, platform_json):
        """
        # insert gamesdb game system
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_games_system_insert(platform_id, platform_name,
                                                       platform_alias, platform_json)
