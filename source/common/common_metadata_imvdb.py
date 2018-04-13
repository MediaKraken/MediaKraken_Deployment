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

import requests

from . import common_global


class CommonMetadataIMVdb(object):
    """
    Class for interfacing with imvdb
    """

    def __init__(self, option_config_json):
        self.headers = {'User-Agent': 'MediaKraken_0.1.6',
                        'IMVDB-APP-KEY': option_config_json['API']['imvdb'],
                        'Accept': 'application/json'}
        self.base_api_url = 'http://imvdb.com/api/v1'

    def com_imvdb_video_info(self, video_id):
        """
        Video info
        """
        resp = requests.post(self.base_api_url + "/video/" + video_id
                             + "?include=sources,credits,bts,featured,popularity,countries,",
                             headers=self.headers)
        common_global.es_inst.com_elastic_index('info', {"imvdb Info Status":
                                                             resp.status_code, 'json': resp.json()})
        return resp.json()

    def com_imvdb_search_video(self, artist_name, song_title):
        """
        Search for video by band name and song title
        """
        resp = requests.post(self.base_api_url + "/search/videos?q="
                             + (artist_name.replace(' ', '+') + '+'
                                + song_title.replace(' ', '+')),
                             headers=self.headers)
        common_global.es_inst.com_elastic_index('info', {"imvdb Video Status":
                                                         resp.status_code, 'json': resp.json()})
        return resp.json()

    def com_imvdb_search_entities(self, artist_name):
        """
        Search by band name
        """
        resp = requests.post(self.base_api_url + "/search/entities?q="
                             + artist_name.replace(' ', '+'), headers=self.headers)
        common_global.es_inst.com_elastic_index('info', {"imvdb Entities Status":
                                                             resp.status_code, 'json': resp.json()})
        return resp.json()
