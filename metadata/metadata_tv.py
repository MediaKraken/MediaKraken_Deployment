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
import json
from guessit import guessit
from common import common_config_ini
from common import common_thetvdb
from common import common_metadata_anidb
from common import common_metadata_imdb
from common import common_metadata_netflixroulette
from common import common_metadata_thetvdb
from common import common_metadata_tv_intro
from common import common_metadata_tv_theme
from common import common_metadata_tvmaze
from . import metadata_nfo_xml

config_handle, option_config_json, db_connection = common_config_ini.com_config_read()

# verify thetvdb key exists for search
if option_config_json['API']['theTVdb'] is not None:
    THETVDB_CONNECTION = common_thetvdb.CommonTheTVDB(option_config_json)
    # show xml downloader and general api interface
    THETVDB_API = common_metadata_thetvdb.CommonMetadataTheTVDB(option_config_json)
else:
    THETVDB_CONNECTION = None


# setup the tvmaze class
if option_config_json['API']['tvmaze'] is not None:
    TVMAZE_CONNECTION = common_metadata_tvmaze.CommonMetadatatvmaze(option_config_json)
else:
    TVMAZE_CONNECTION = None


def tv_search_tvdb(db_connection, file_name):
    """
    # tvdb search
    """
    metadata_uuid = None
    if THETVDB_CONNECTION is not None:
        if 'year' in file_name:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],\
                file_name['year'], tvdb_id, lang_code, True))
        else:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],\
                None, tvdb_id, lang_code, True))
        logging.debug("response: %s", tvdb_id)
        if tvdb_id is not None:
            # since there has been NO match whatsoever.....can "wipe" out everything
            media_id_json = json.dumps({'thetvdb': tvdb_id})
            logging.debug("dbjson: %s", media_id_json)
            # check to see if metadata exists for TVDB id
            metadata_uuid = db_connection.db_metatv_guid_by_tvdb(tvdb_id)
            logging.debug("db result: %s", metadata_uuid)
    return metadata_uuid


def tv_fetch_save_tvdb(db_connection, tvdb_id):
    """
    # tvdb data fetch
    """
    metadata_uuid = None
    # fetch XML zip file
    xml_show_data, xml_actor_data, xml_banners_data\
        = THETVDB_API.com_meta_thetvdb_get_zip_by_id(tvdb_id)
    if xml_show_data is not None:
        # insert
        image_json = {'Images': {'thetvdb': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
        series_id_json = json.dumps({'imdb': xml_show_data['Data']['Series']['imdb_ID'],\
            'thetvdb': str(tvdb_id), 'zap2it': xml_show_data['Data']['Series']['zap2it_id']})
        metadata_uuid = db_connection.db_metatvdb_insert(series_id_json,\
            xml_show_data['Data']['Series']['SeriesName'], json.dumps({'Meta': {'thetvdb':\
            {'Meta': xml_show_data['Data'], 'Cast': xml_actor_data,\
            'Banner': xml_banners_data}}}), json.dumps(image_json))
        # insert cast info
        if xml_actor_data is not None:
            db_connection.db_meta_person_insert_cast_crew('thetvdb',\
                xml_actor_data['Actor'])
    return metadata_uuid


def metadata_tv_lookup(db_connection, media_file_path, download_que_json, download_que_id):
    """
    Lookup tv metadata
    """
    # check for same show variables
    if not hasattr(metadata_tv_lookup, "metadata_last_id"):
        metadata_tv_lookup.metadata_last_id = None  # it doesn't exist yet, so initialize it
        metadata_tv_lookup.metadata_last_title = None
        metadata_tv_lookup.metadata_last_year = None
        metadata_tv_lookup.metadata_last_imdb = None
        metadata_tv_lookup.metadata_last_tvdb = None
    # determine file name/etc for handling name/year skips
    file_name = guessit(media_file_path)
    # check for dupes by name/year
    if 'year' in file_name:
        if file_name['title'] == metadata_tv_lookup.metadata_last_title\
                and file_name['year'] == metadata_tv_lookup.metadata_last_year:
            return metadata_tv_lookup.metadata_last_id
    elif file_name['title'] == metadata_tv_lookup.metadata_last_title:
        return metadata_tv_lookup.metadata_last_id
    # grab by nfo/xml data
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file(media_file_path)
    # lookup by id's occur in nfo/xml code below!
    metadata_uuid, imdb_id, tvdb_id, rt_id = metadata_nfo_xml.nfo_xml_db_lookup_tv(db_connection,\
        nfo_data, xml_data, download_que_json, download_que_id)
    logging.debug("tv look: %s %s %s %s", metadata_uuid, imdb_id, tvdb_id, rt_id)
    if metadata_uuid is None:
        # if same as last, return last id and save lookup
        # check these dupes as the nfo/xml files might not exist to pull the metadata id from
        if imdb_id is not None and imdb_id == metadata_tv_lookup.metadata_last_imdb:
            return metadata_tv_lookup.metadata_last_id
        if tvdb_id is not None and tvdb_id == metadata_tv_lookup.metadata_last_tvdb:
            return metadata_tv_lookup.metadata_last_id
        # search thetvdb as the episodes will be under tv show for class per libraries
        # indiv eps is bad lookup - metadata_uuid, imdb_id, tvdb_id\
            #= metadata_nfo_xml.nfo_xml_db_lookup_tv(db_connection, media_file_path,\
            #metadata_nfo_xml.nfo_xml_file(media_file_path))
        # lookup on local db via name, year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(file_name['title'],\
                file_name['year'])
        else:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(file_name['title'],\
                None)
        if metadata_uuid is None:
            # search thetvdb since not matched above via DB
            # TODO insert que search record
            pass
    # set last values to negate lookups for same show
    metadata_tv_lookup.metadata_last_id = metadata_uuid
    metadata_tv_lookup.metadata_last_title = file_name['title']
    try:
        metadata_tv_lookup.metadata_last_year = file_name['year']
    except:
        metadata_tv_lookup.metadata_last_year = None
    metadata_tv_lookup.metadata_last_imdb = imdb_id
    metadata_tv_lookup.metadata_last_tvdb = tvdb_id
    return metadata_uuid
