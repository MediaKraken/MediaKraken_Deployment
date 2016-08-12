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
import json
import requests


class CommonIMVDb(object):
    """
    Class for interfacing with imvdb
    """
    def __init__(self, imvdb_api_key):
        self.headers = {'User-Agent': 'MediaKraken_0.1.1',
                        'IMVDB-APP-KEY': imvdb_api_key,
                        'Accept': 'application/json'}
        self.BASE_API_URL = 'http://imvdb.com/api/v1'


    def com_imvdb_video_info(self, video_id):
        resp = requests.post(self.BASE_API_URL + "/video/" + video_id\
            + "?include=sources,credits,bts,featured,popularity,countries,", headers=self.headers)
        logging.debug("IMVDb Info Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_imvdb_search_video(self, artist_name, song_title):
        """
        Search for video by band name and song title
        """
        resp = requests.post(self.BASE_API_URL + "/search/videos?q="\
            + (artist_name.replace(' ', '+') + '+' + song_title.replace(' ', '+')),\
            headers=self.headers)
        logging.debug("IMVDb Video Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_imvdb_search_entities(self, artist_name):
        """
        Search by band name
        """
        resp = requests.post(self.BASE_API_URL + "/search/entities?q="\
            + artist_name.replace(' ', '+'), headers=self.headers)
        logging.debug("IMVDb Entities Status: %s-%s", resp.status_code, resp.json())
        return resp.json()
