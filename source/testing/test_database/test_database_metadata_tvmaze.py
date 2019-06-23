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


class TestDatabaseMetadatatvmaze:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # metadata changed date by uuid
    # def db_metatvmaze_changed_uuid(self, maze_uuid):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("series_id_json", "tvmaze_name", "show_detail", "image_json"), [
        (json.dumps({'tvmaze': 34}), "Test", json.dumps(
            {'Test': 'Moo'}), json.dumps({'Tt': 'M'})),
        (json.dumps({'tvmaze': 3}), "Tst", json.dumps({'Tst': 'Moo'}), json.dumps({'T': 'M'}))])
    def test_db_meta_tvmaze_insert(self, series_id_json, tvmaze_name, show_detail, image_json):
        """
        # insert
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_meta_tvmaze_insert(series_id_json, tvmaze_name,
                                                                 show_detail, image_json)

    # updated
    @pytest.mark.parametrize(("series_id_json", "tvmaze_name", "show_detail", "tvmaze_id"), [
        (json.dumps({'tvmaze': 34}), "Test", json.dumps({'Test': 'Moo'}), 3),
        (json.dumps({'tvmaze': 3}), "Tst", json.dumps({'Tst': 'Moo'}), 4)])
    def test_db_meta_tvmaze_update(self, series_id_json, tvmaze_name, show_detail, tvmaze_id):
        self.db_connection.db_rollback()
        self.db_connection.db_meta_tvmaze_update(series_id_json, tvmaze_name,
                                                 show_detail, tvmaze_id)
