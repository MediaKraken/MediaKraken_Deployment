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
from common import common_metadata_anidb
from . import metadata_nfo_xml


option_config_json, db_connection = common_config_ini.com_config_read()


# verify provider key exists
if option_config_json['API']['AniDB'] is not None:
    # setup the connection class
    ANIDB_CONNECTION = common_metadata_anidb.CommonMetadataANIdb(option_config_json)
else:
    ANIDB_CONNECTION = None


def metadata_anime_lookup(db_connection, media_file_path, download_que_json, download_que_id,\
                          file_name):
    """
    Check for anime in tv sections of the metadata providers
    """
    if not hasattr(metadata_anime_lookup, "metadata_last_id"):
        metadata_anime_lookup.metadata_last_id = None # it doesn't exist yet, so initialize it
        metadata_anime_lookup.metadata_last_title = None
        metadata_anime_lookup.metadata_last_year = None
        metadata_anime_lookup.metadata_last_imdb = None
        metadata_anime_lookup.metadata_last_tmdb = None
        metadata_anime_lookup.metadata_last_rt = None
        metadata_anime_lookup.metadata_last_anidb = None
    metadata_uuid = None # so not found checks verify later
    logging.info('meta anime look filename: %s', file_name)
    # check for dupes by name/year
    if 'year' in file_name:
        if file_name['title'] == metadata_anime_lookup.metadata_last_title\
                and file_name['year'] == metadata_anime_lookup.metadata_last_year:
            db_connection.db_download_delete(download_que_id)
            logging.info('meta anime return 1 %s',  metadata_anime_lookup.metadata_last_id)
            # don't need to set last......since they are equal
            return metadata_anime_lookup.metadata_last_id
    elif file_name['title'] == metadata_anime_lookup.metadata_last_title:
        db_connection.db_download_delete(download_que_id)
        logging.info('meta anime return 2 %s',  metadata_anime_lookup.metadata_last_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id
    # determine provider id's from nfo/xml if they exist
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file(media_file_path)
    imdb_id, tmdb_id, rt_id, anidb_id = metadata_nfo_xml.nfo_xml_id_lookup(nfo_data, xml_data)
    logging.info("meta anime look: %s %s %s %s %s %s %s %s", imdb_id, tmdb_id, rt_id, anidb_id,\
        metadata_anime_lookup.metadata_last_imdb, metadata_anime_lookup.metadata_last_tmdb,\
        metadata_anime_lookup.metadata_last_rt, metadata_anime_lookup.metadata_last_anidb)
    # if same as last, return last id and save lookup
    if imdb_id is not None and imdb_id == metadata_anime_lookup.metadata_last_imdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id
    if tmdb_id is not None and tmdb_id == metadata_anime_lookup.metadata_last_tmdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id
    if rt_id is not None and rt_id == metadata_anime_lookup.metadata_last_rt:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id
    if anidb_id is not None and anidb_id == metadata_anime_lookup.metadata_last_anidb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id
    # if ids from nfo/xml, query local db to see if exist
    if tmdb_id is not None:
        metadata_uuid = db_connection.db_meta_guid_by_tmdb(tmdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_imdb(imdb_id)
    if rt_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_rt(rt_id)
    if anidb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_anidb(anidb_id)
    # if ids from nfo/xml on local db
    logging.info("meta anime metadata_uuid A: %s", metadata_uuid)
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last name/year id's
    else:
        # id is known from nfo/xml but not in db yet so fetch data
        if tmdb_id is not None or imdb_id is not None:
            if tmdb_id is not None:
                dl_meta = db_connection.db_download_que_exists(download_que_id,\
                                                               'themoviedb', str(tmdb_id))
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(tmdb_id)})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('themoviedb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
            else:
                dl_meta = db_connection.db_download_que_exists(download_que_id,\
                    'themoviedb', imdb_id)
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': imdb_id})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('themoviedb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
        if metadata_uuid is None and tvmaze_id is not None:
            dl_meta = db_connection.db_download_que_exists(download_que_id,\
                                                           'tvmaze', str(anidb_id))
            if dl_meta is None:
                metadata_uuid = download_que_json['MetaNewID']
                download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(anidb_id)})
                db_connection.db_download_update(json.dumps(download_que_json),\
                    download_que_id)
                # set provider last so it's not picked up by the wrong thread too early
                db_connection.db_download_update_provider('tvmaze', download_que_id)
            else:
                db_connection.db_download_delete(download_que_id)
                metadata_uuid = dl_meta
        if metadata_uuid is None and thetvdb_id is not None:
            dl_meta = db_connection.db_download_que_exists(download_que_id,\
                                                           'thetvdb', str(anidb_id))
            if dl_meta is None:
                metadata_uuid = download_que_json['MetaNewID']
                download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(anidb_id)})
                db_connection.db_download_update(json.dumps(download_que_json),\
                    download_que_id)
                # set provider last so it's not picked up by the wrong thread too early
                db_connection.db_download_update_provider('thetvdb', download_que_id)
            else:
                db_connection.db_download_delete(download_que_id)
                metadata_uuid = dl_meta
        if metadata_uuid is None and anidb_id is not None:
            dl_meta = db_connection.db_download_que_exists(download_que_id,\
                                                           'anidb', str(anidb_id))
            if dl_meta is None:
                metadata_uuid = download_que_json['MetaNewID']
                download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(anidb_id)})
                db_connection.db_download_update(json.dumps(download_que_json),\
                    download_que_id)
                # set provider last so it's not picked up by the wrong thread too early
                db_connection.db_download_update_provider('anidb', download_que_id)
            else:
                db_connection.db_download_delete(download_que_id)
                metadata_uuid = dl_meta
    logging.info("meta anime metadata_uuid B: %s", metadata_uuid)
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        logging.info("meta anime db lookup")
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'],\
                file_name['year'])
        else:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'], None)
        logging.info("meta movie db meta: %s", metadata_uuid)
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            # no matches by name/year
            # search themoviedb since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),\
                download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('themoviedb', download_que_id)
    logging.info("meta anime metadata_uuid c: %s", metadata_uuid)
    # set last values to negate lookups for same title/show
    metadata_anime_lookup.metadata_last_id = metadata_uuid
    metadata_anime_lookup.metadata_last_title = file_name['title']
    try:
        metadata_anime_lookup.metadata_last_year = file_name['year']
    except:
        metadata_anime_lookup.metadata_last_year = None
    metadata_anime_lookup.metadata_last_imdb = imdb_id
    metadata_anime_lookup.metadata_last_tmdb = tmdb_id
    metadata_anime_lookup.metadata_last_rt = rt_id
    metadata_anime_lookup.metadata_last_anidb = anidb_id
    return metadata_uuid
