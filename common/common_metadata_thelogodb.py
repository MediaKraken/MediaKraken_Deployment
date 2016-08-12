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
import logging
import os
import json
import com_Metadata
import common_network


class CommonTheLogoDB(object):
    """
    Class for interfacing with TheLogoDB
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.exists("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../../MediaKraken_Server/MediaKraken.ini")
        self.API_KEY = Config.get('API', 'TheLogoDB').strip()


    def com_TheLogoDB_Fetch_Latest(self):
        """
        Grab newest releases
        """
        return json.loads(com_network.MK_Network_Fetch_From_URL('http://www.thelogodb.com/api/json/v1/' + self.API_KEY + '/tvlatest.php', None))
