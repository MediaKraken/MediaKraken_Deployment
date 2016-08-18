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
import database as database_base


class TestDatabaseDownload(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()


    # create/insert a download
    # def db_download_insert(self, provider, down_json):
#        self.db_connection.db_rollback()


#    ## read the download
# this no longer exists
#    def test_db_download_read(self):
#        self.db_connection.db_Download_Read()
#        self.db_connection.db_rollback()


    @pytest.mark.parametrize(("provider_name"), [
        ('themoviedb'),
        ('fakeprovider')])
    def test_db_download_read_provider(self, provider_name):
        """
        # read the downloads by provider
        """
        self.db_connection.db_rollback()
        self.db_connection.db_download_read_provider(provider_name)


    # remove download
    # def db_download_delete(self, guid):
#        self.db_connection.db_rollback()


    # update provdier
    # def db_download_update_provider(self, provider_name, guid):
#        self.db_connection.db_rollback()


    # def db_download_update(self, update_json, guid):
#        self.db_connection.db_rollback()
