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
#import logging
import os
import json
#import common_metadata
import common_network


class CommonMetadataTheLogoDB(object):
    """
    Class for interfacing with thelogodb
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.exists("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../../MediaKraken_Server/MediaKraken.ini")
        self.API_KEY = Config.get('API', 'thelogodb').strip()


    def com_thelogodb_fetch_latest(self):
        """
        Grab newest releases
        """
        return json.loads(common_network.mk_network_fetch_from_url(\
            'http://www.thelogodb.com/api/json/v1/' + self.API_KEY + '/tvlatest.php', None))
