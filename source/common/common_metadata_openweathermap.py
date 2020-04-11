"""
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import gzip
import json
import urllib.error
import urllib.parse
import urllib.request

from . import common_network


class CommonMetadataOpenweatherMap:
    """
    Class for interfacing with OpenweatherMap
    """

    def __init__(self, option_config_json):
        self.api_key = option_config_json['API']['openweathermap']

    def com_openweathermap(self, city):
        """
        Grab the weather for city
        """
        return json.load(
            urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s'
                                   % (city, self.api_key)))

    def com_openweathermap_fetch_city(self):
        """
        Fetch city list
        """
        common_network.mk_network_fetch_from_url(
            'http://bulk.openweathermap.org/sample/city.list.json.gz', 'city.list.json.gz')

    def com_openweathermap_add_city(self):
        """
        Add the cities from the list
        """
        with gzip.open('city.list.json.gz', 'rb') as file_handle:
            file_content = file_handle.read()
        for json_item in file_content:
            print(json_item, flush=True)
        file_handle.close()
