"""
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
"""

import json
import os
import time

from . import common_file
from . import common_global
from . import common_network


def mk_manami_fetch_json():
    """
    Fetch the anime list by manami for thetvdb crossreference
    """
    # grab from github via direct raw link
    if not os.path.isfile('./cache/anime-manami-list.json') \
            or common_file.com_file_modification_timestamp('./cache/anime-manami-list.json') \
            < (time.time() - (7 * 86400)):
        common_network.mk_network_fetch_from_url(
            'https://github.com/manami-project/anime-offline-database/raw/master/anime-offline-database.json',
            './cache/anime-manami-list.json')


def mk_manami_anime_list_parse(file_name='./cache/anime-manami-list.json'):
    """
    Parse the anime list
    """
    anime_cross_reference = []
    file_handle = open(file_name, 'r')
    itemlist = json.loads(file_handle.read())
    file_handle.close()
    for anime_data in itemlist['data']:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'data': anime_data})
    #     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'key': list(anime_data.keys())})

    # data chunks below
    # "sources": [
    #     "https://myanimelist.net/anime/38288"
    # ],
    # "type": "OVA",
    # "title": "Kaih\u014d Sh\u014djo",
    # "picture": "https://myanimelist.cdn-dena.com/images/anime/1182/93652.jpg",
    # "relations": [
    #
    # ],
    # "id": "7b95ed68-7215-4bb0-9c0c-c71edaa5ee68",
    # "thumbnail": "https://myanimelist.cdn-dena.com/images/anime/1182/93652t.jpg",
    # "episodes": 2,
    # "synonyms": [
    #     "Liberation Maiden",
    #     "\u89e3\u653e\u5c11\u5973"
    # ]

    #     anime_cross_reference.append((anime_data['@anidbid'], tvdbid, imdbid,
    #                                   default_tvseason, mapping_data, before_data))
    # return anime_cross_reference
