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
from common import common_cloud_onedrive
from common import common_config_ini


class TestCommonCloudOneDrive(object):

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.onedrive_connection = common_cloud_onedrive.CommonCloudOneDrive(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass
