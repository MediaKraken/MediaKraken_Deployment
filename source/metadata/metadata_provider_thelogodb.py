"""
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
"""

import json

from common import common_network

"""
Website is down for the count!!!
Website is down for the count!!!
Website is down for the count!!!
"""


class CommonMetadataTheLogoDB:
    """
    Class for interfacing with thelogodb
    """

    def __init__(self, option_config_json):
        self.logo_api_key = option_config_json['API']['thelogodb']

    def com_thelogodb_fetch_latest(self):
        """
        Grab newest releases
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'http://www.thelogodb.com/api/json/v1/' + self.logo_api_key + '/tvlatest.php', None))
