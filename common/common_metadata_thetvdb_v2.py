'''
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
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import requests

'''
https://api.thetvdb.com/swagger#/
'''


class CommonMetadataTheTVDBv2(object):
    """
    Class for interfacing with TheTVDB with swagger
    """
    def __init__(self, option_config_json):
        self.headers = {'apikey': option_config_json['API']['thetvdb'],
#                        'username': None, 'userkey': None,
                        'Accept': 'application/json'}
        self.base_api_url = 'https://api.thetvdb.com/'


    def com_meta_thetvdbv2_login(self):
        print('header %s', self.headers)
        resp = requests.post(self.base_api_url + "login", headers=self.headers)
        logging.info("thetvdbv2_login Info Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_meta_thetvdbv2_language(self):
        resp = requests.post(self.base_api_url + "languages", headers=self.headers)
        logging.info("thetvdbv2_lang Info Status: %s-%s", resp.status_code, resp.json())
        return resp.json()



