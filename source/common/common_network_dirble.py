'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import requests


class CommonNetworkDirble:
    """
    Class for interfacing with Dirble
    """

    def __init__(self, option_config_json):
        self.API_KEY = option_config_json['API']['dirble']
        self.BASE_URL = 'http://api.dirble.com/v2/'

    def com_dirble_station_list(self):
        """
        Fetch station list
        """
        return requests.get(self.BASE_URL + 'stations&token=%s' % (self.API_KEY,))

    def com_dirble_recent_station_list(self):
        """
        Fetch recent station list
        """
        return requests.get(self.BASE_URL + 'stations/recent&token=%s' % (self.API_KEY,))

    def com_dirble_category_list(self):
        """
        Fetch category list
        """
        return requests.get(self.BASE_URL + 'stations/categories&token=%s' % (self.API_KEY,))

    def com_dirble_category_station_list(self, category_id):
        """
        Fetch category station list
        """
        return requests.get(
            self.BASE_URL + 'category/%s/stations&token=%s' % (category_id, self.API_KEY))
