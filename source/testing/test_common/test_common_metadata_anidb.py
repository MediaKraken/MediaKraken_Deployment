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

sys.path.append('.')
from common import common_metadata_anidb


class TestCommonMetadataAnidb:

    @classmethod
    def setup_class(self):
        self.anidb_connection = common_metadata_anidb.CommonMetadataANIdb()

    @classmethod
    def teardown_class(self):
        pass

    # fetch the tarball of anime titles
    # def com_net_anidb_fetch_titles_file(self, data_type='dat'):

    # save anidb title data to database
    # def com_net_anidb_save_title_data_to_db(self, title_file):

    # find AID by title
    # def com_net_anidb_aid_by_title(self, title_to_search):

    # remote api calls
    # def com_net_anidb_connect(self, user_name, user_password):

    # logout of anidb
    def test_com_net_anidb_logout(self):
        """
        Test function
        """
        self.anidb_connection.com_net_anidb_logout()

    # close the anidb connect and stop the thread
    def test_com_net_anidb_stop(self):
        """
        Test function
        """
        self.anidb_connection.com_net_anidb_stop()
