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
from common import common_config_ini
from common import common_metadata_thetvdb


class TestCommonMetadataTheTVDB:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.db_connection = common_metadata_thetvdb.CommonMetadataTheTVDB(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # def com_meta_TheTVDB_Updates(self, frequency='day'):

    # def com_meta_TheTVDB_Get_ZIP_by_ID(self, tv_show_id, lang_code='en'):

    def test_com_meta_thetvdb_get_server_epoc_time(self):
        """
        Test function
        """
        self.db_connection.com_meta_thetvdb_get_server_epoc_time()

# def com_meta_TheTVDB_Updates_by_Epoc(self, epoc_timestamp):


# def com_meta_TheTVDB_Update_Series_Read(self, tv_show_id, lang_code = 'en'):


# def com_meta_TheTVDB_Update_Episode_Read(self, tv_eps_id, lang_code = 'en'):
