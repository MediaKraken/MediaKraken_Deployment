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

import json
import logging
import requests


class MK_Common_IMVDb_API:
    def __init__(self, imvdb_api_key):
        self.headers = {'User-Agent': 'MediaKraken_0.1.1',
                        'IMVDB-APP-KEY': imvdb_api_key,
                        'Accept': 'application/json'}
        self.BASE_API_URL = 'http://imvdb.com/api/v1'


    def MK_Common_IMVDb_Video_Info(self, video_id):
        resp = requests.post(self.BASE_API_URL + "/video/" + video_id + "?include=sources,credits,bts,featured,popularity,countries,", headers=self.headers)
        logging.debug("IMVDb Info Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def MK_Common_IMVDb_Search_Video(self, artist_name, song_title):
        resp = requests.post(self.BASE_API_URL + "/search/videos?q=" + (artist_name.replace(' ', '+') + '+' + song_title.replace(' ', '+')), headers=self.headers)
        logging.debug("IMVDb Video Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def MK_Common_IMVDb_Search_Entities(self, artist_name):
        resp = requests.post(self.BASE_API_URL + "/search/entities?q=" + artist_name.replace(' ', '+'), headers=self.headers)
        logging.debug("IMVDb Entities Status: %s-%s", resp.status_code, resp.json())
        return resp.json()
