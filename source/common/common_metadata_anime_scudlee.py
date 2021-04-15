"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

import os
import time
from xml.dom import minidom

import xmltodict
from common import common_logging_elasticsearch_httpx

from . import common_file
from . import common_network


def mk_scudlee_fetch_xml():
    """
    Fetch the anime list by scudlee for thetvdb crossreference
    """
    # grab from github via direct raw link
    if not os.path.isfile('./cache/anime-list.xml') \
            or common_file.com_file_modification_timestamp('./cache/anime-list.xml') \
            < (time.time() - (7 * 86400)):
        common_network.mk_network_fetch_from_url(
            'https://github.com/ScudLee/anime-lists/raw/master/anime-list.xml',
            './cache/anime-list.xml')
    if not os.path.isfile('./cache/anime-movieset-list.xml') \
            or common_file.com_file_modification_timestamp('./cache/anime-movieset-list.xml') \
            < (time.time() - (7 * 86400)):
        common_network.mk_network_fetch_from_url(
            'https://github.com/ScudLee/anime-lists/raw/master/anime-movieset-list.xml',
            './cache/anime-movieset-list.xml')


def mk_scudlee_anime_list_parse(file_name='./cache/anime-list.xml'):
    """
    Parse the anime list
    """
    anime_cross_reference = []
    file_handle = open(file_name, 'r')
    itemlist = xmltodict.parse(file_handle.read())
    file_handle.close()
    for anime_data in itemlist['anime-list']['anime']:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'data': anime_data})
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'key': list(anime_data.keys())})
        try:
            # to make sure not web, etc
            tvdbid = str(int(anime_data['@tvdbid']))
        except:
            tvdbid = None
        try:
            imdbid = anime_data['@imdbid']
            if imdbid == 'unknown':
                imdbid = None
        except KeyError:
            imdbid = None
        try:
            default_tvseason = anime_data['@defaulttvdbseason']
        except KeyError:
            default_tvseason = None
        try:
            mapping_data = anime_data['mapping-list']
        except KeyError:
            mapping_data = None
        try:
            before_data = anime_data['before']
        except KeyError:
            before_data = None
        anime_cross_reference.append((anime_data['@anidbid'], tvdbid, imdbid,
                                      default_tvseason, mapping_data, before_data))
    return anime_cross_reference


def mk_scudlee_anime_set_parse(file_name='./cache/anime-movieset-list.xml'):
    """
    Parse the movieset list
    """
    itemlist = minidom.parse(file_name).getElementsByTagName('set')
    collection_list = []
    for set_data in itemlist:
        indiv_collection_list = []
        for anime_data in set_data.getElementsByTagName('anime'):
            indiv_collection_list.append(
                anime_data.attributes['anidbid'].value)
        indiv_titles_list = []
        for anime_data in set_data.getElementsByTagName('title'):
            indiv_titles_list.append(anime_data.firstChild.nodeValue)
        collection_list.append((indiv_collection_list, indiv_titles_list))
    return collection_list
