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
from common import common_network_flickr


class TestCommonFlickr:

    @classmethod
    def setup_class(self):
        self.db_connection = common_network_flickr.CommonNetworkFlickr()

    @classmethod
    def teardown_class(self):
        pass

# class com_Flickr_API:
#    def __init__(self, api_key, api_secret):
