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
import logging # pylint: disable=W0611
import os
from common import common_file
from common import common_file_extentions
import xmltodict


def nfo_xml_file(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    # TODO search for tvinfo.nfo and use ID from that if exists
    xml_data = None
    # check for NFO or XML as no need to do lookup if ID found in it
    try: # pull the "real" extention
        ext_check = media_file_path[-4:].lower().split(".")[-1]
    except:
        ext_check = None
    if ext_check in common_file_extentions.SUBTITLE_EXTENSION:
        # need to chop off the lang too, the split works even with no .lang in name
        nfo_file_check = media_file_path.rsplit('.', 2)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 2)[0] + '.xml'
    else:
        nfo_file_check = media_file_path.rsplit('.', 1)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 1)[0] + '.xml'
    logging.debug('nfo file: %s', nfo_file_check)
    logging.debug('xml file: %s', xml_file_name)
    if os.path.isfile(nfo_file_check): # check for nfo
        nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
    else:
        nfo_data = None
        # only check for xml if nfo doesn't exist
        if os.path.isfile(xml_file_name): # check for xml
            xml_data = xmltodict.parse(common_file.com_file_load_data(xml_file_name, False))
        elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(media_file_path)),\
                'movie.xml')):
            xml_data = xmltodict.parse(common_file.com_file_load_data(os.path.join(\
                os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml'), False))
    return nfo_data, xml_data


def nfo_xml_id_lookup(nfo_data, xml_data):
    """
    Lookup by id's in nfo/xml files
    """
    imdb_id = None
    tmdb_id = None
    rt_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try: # not all will have imdb
            imdb_id = nfo_data['movie']['imdbid']
        except:
            pass
        try: # not all nfo's have the movie/tmdb
            tmdb_id = xml_data['movie']['tmdbid']
        except:
            pass
        # RT
    if xml_data is not None:
        if imdb_id is None:
            try: # not all xmls's will have the imdb
                imdb_id = nfo_data['movie']['imdbid']
            except:
                pass
        if tmdb_id is None:
            try: # not all xml's have the movie/tmdb
                tmdb_id = xml_data['movie']['tmdbid']
            except:
                pass
        # RT
    return (imdb_id, tmdb_id, rt_id)


def nfo_xml_id_lookup_tv(nfo_data, xml_data):
    """
    Look up id's in nfo/xml lookup for tv
    """
    imdb_id = None
    tvdb_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try:
            tvdb_id = nfo_data['episodedetails']['tvdbid']
        except:
            pass
        try:
            imdb_id = nfo_data['episodedetails']['imdbid']
        except:
            pass
    # RT
    if xml_data is not None and imdb_id is None and tvdb_id is None:
        try:
            tvdb_id = xml_data['episodedetails']['tvdbid']
        except:
            pass
        try:
            imdb_id = xml_data['episodedetails']['imdbid']
        except:
            pass
    # RT
    return (imdb_id, tvdb_id)
