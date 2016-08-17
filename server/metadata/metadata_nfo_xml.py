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
import os
import sys
sys.path.append("../common")
sys.path.append("../server") # for db import
from common import common_file
import xmltodict


def nfo_xml_file(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    # TODO search for tvinfo.nfo and use ID from that if exists
    xml_data = None
    # check for NFO as no need to do lookup  media_file_path = mm_media_path
    nfo_file_check = os.path.join(os.path.dirname(os.path.abspath(media_file_path)),\
        os.path.basename(media_file_path).rsplit('.', 1)[0] + '.nfo')
    if os.path.isfile(nfo_file_check): # check for nfo
        nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
    else:
        nfo_data = None
        # only check for xml if nfo doesn't exist
        xml_file_name = os.path.join(os.path.dirname(os.path.abspath(media_file_path)),\
            os.path.basename(media_file_path).rsplit('.', 1)[0] + '.xml')
        if os.path.isfile(xml_file_name): # check for xml
            xml_data = xmltodict.parse(common_file.com_file_load_data(xml_file_name, False))
        elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(media_file_path)),\
                'movie.xml')):
            xml_data = xmltodict.parse(common_file.com_file_load_data(os.path.join(\
                os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml'), False))
    return nfo_data, xml_data


def nfo_xml_db_lookup(db_connection, nfo_data, xml_data, download_que_json, download_que_id):
    """
    Lookup by id's in nfo/xml files
    """
    metadata_uuid = None
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
        # TODO RT
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
        # TODO RT
    if tmdb_id is not None:
        metadata_uuid = db_connection.srv_db_meta_guid_by_tmdb(tmdb_id)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': tmdb_id})
            db_connection.srv_db_download_update(json.dumps(download_que_json), download_que_id)
            db_connection.srv_db_download_update_Provider('themoviedb', download_data['mdq_id'])
            metadata_uuid = download_que_json['MetaNewID']
    if metadata_uuid is None and imdb_id is not None:
        metadata_uuid = db_connection.srv_db_meta_guid_by_imdb(imdb_id)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': imdb_id})
            db_connection.srv_db_download_update(json.dumps(download_que_json), download_que_id)
            db_connection.srv_db_download_update_Provider('imdb', download_data['mdq_id'])
            metadata_uuid = download_que_json['MetaNewID']
    if metadata_uuid is None and rt_id is not None:
        metadata_uuid = db_connection.srv_db_meta_guid_by_rt(rt_id)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': rt_id})
            db_connection.srv_db_download_update(json.dumps(download_que_json), download_que_id)
            db_connection.srv_db_download_update_Provider('rotten_tomatoes',\
                download_data['mdq_id'])
            metadata_uuid = download_que_json['MetaNewID']
    return (metadata_uuid, imdb_id, tmdb_id, rt_id)


def nfo_xml_db_lookup_tv(db_connection, nfo_data, xml_data, download_que_json, download_que_id):
    """
    Look up id's in nfo/xml db lookup for tv
    """
    metadata_uuid = None
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
    if xml_data is not None and imdb_id is None and tvdb_id is None:
        try:
            tvdb_id = xml_data['episodedetails']['tvdbid']
        except:
            pass
        try:
            imdb_id = xml_data['episodedetails']['imdbid']
        except:
            pass
    # TODO RT
    if tvdb_id is not None:
        metadata_uuid = db_connection.srv_db_metatv_guid_by_tvdb(tvdb_id)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': tvdb_id})
            db_connection.srv_db_download_update(json.dumps(download_que_json), download_que_id)
            db_connection.srv_db_download_update_Provider('thetvdb', download_data['mdq_id'])
            metadata_uuid = download_que_json['MetaNewID']
    if metadata_uuid is None and imdb_id is not None:
        metadata_uuid = db_connection.srv_db_metaTV_guid_by_imdb(imdb_id)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': imdb_id})
            db_connection.srv_db_download_update(json.dumps(download_que_json), download_que_id)
            db_connection.srv_db_download_update_Provider('imdb', download_data['mdq_id'])
            metadata_uuid = download_que_json['MetaNewID']
    return (metadata_uuid, imdb_id, tvdb_id)
