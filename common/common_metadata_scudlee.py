'''
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
'''

import sys
import logging
import time
import os
from xml.dom import minidom
import MK_Common_File
import MK_Common_Network


def MK_Scudlee_Fetch_XML():
    """
    Fetch the anime list by scudlee for thetvdb crossreference
    """
    # grab from github via direct raw link
    if not os.path.isfile('./cache/anime-list.xml') or MK_Common_File.MK_Common_File_Modification_Timestamp('./cache/anime-list.xml') < (time.time() - (30 * 86400)):
        MK_Common_Network.MK_Network_Fetch_From_URL('https://github.com/ScudLee/anime-lists/raw/master/anime-list.xml', './cache/anime-list.xml')
    if not os.path.isfile('./cache/anime-movieset-list.xml') or MK_Common_File.MK_Common_File_Modification_Timestamp('./cache/anime-movieset-list.xml') < (time.time() - (30 * 86400)):
        MK_Common_Network.MK_Network_Fetch_From_URL('https://github.com/ScudLee/anime-lists/raw/master/anime-movieset-list.xml', './cache/anime-movieset-list.xml')


def MK_Scudlee_Anime_List_Parse(file_name=None):
    """
    Parse the anime list
    """
    anime_cross_reference = []
    if file_name is None:
        file_name = './cache/anime-list.xml'
    itemlist = minidom.parse(file_name).getElementsByTagName('anime')
    for anime_data in itemlist:
        anidbid = anime_data.attributes['anidbid'].value
        tvdbid = anime_data.attributes['tvdbid'].value
        try:
            imdbid = anime_data.attributes['imdbid'].value
        except:
            # imdbid is not gaurenteed to be there
            imdbid = None
        default_tvseason = None
        try:
            default_tvseason = anime_data.attributes['defaulttvdbseason'].value
        except:
            # default season not gaurenteed to be there
            pass
        anime_cross_reference.append((anidbid, tvdbid, imdbid, default_tvseason))
    return anime_cross_reference


def MK_Scudlee_Anime_Set_Parse(file_name=None):
    """
    Parse the movieset list
    """
    if file_name is None:
        file_name = './cache/anime-movieset-list.xml'
    itemlist = minidom.parse(file_name).getElementsByTagName('set')
    collection_list = []
    for set_data in itemlist:
        indiv_collection_list = []
        for anime_data in set_data.getElementsByTagName('anime'):
            indiv_collection_list.append(anime_data.attributes['anidbid'].value)
        indiv_titles_list = []
        for anime_data in set_data.getElementsByTagName('title'):
            indiv_titles_list.append(anime_data.firstChild.nodeValue)
        collection_list.append((indiv_collection_list, indiv_titles_list))
    return collection_list
