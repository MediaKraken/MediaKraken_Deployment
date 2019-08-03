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
from common import common_global


class TestDatabaseDownload:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_download_insert(self):
        """
        # create/insert a download
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_download_insert('themovedb',
                                                              common_global.DLMediaType.Movie.value,
                                                              json.dumps({'test': 234}))

    @pytest.mark.parametrize(("provider_name"), [
        ('themoviedb'),
        ('fakeprovider')])
    def test_db_download_read_provider(self, provider_name):
        """
        # read the downloads by provider
        """
        self.db_connection.db_rollback()
        self.db_connection.db_download_read_provider(provider_name)

    def test_db_download_update_provider(self):
        """
        # update provider
        """
        self.db_connection.db_rollback()
        self.db_connection.db_download_update_provider(
            'thetvdb', self.new_guid)

    def test_db_download_update(self):
        """
        Update the json for download
        """
        self.db_connection.db_rollback()
        self.db_connection.db_download_update(
            json.dumps({'test2': 23}), self.new_guid)

    def test_db_download_delete(self):
        """
        # remove download
        """
        self.db_connection.db_rollback()
        self.db_connection.db_download_delete(self.new_guid)
