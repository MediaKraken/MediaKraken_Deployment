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

option_config_json, db_connection = common_config_ini.com_config_read()

# verify thetvdb key exists for search
if option_config_json['API']['thetvdb'] is not None:
    THETVDB_CONNECTION = common_thetvdb.CommonTheTVDB(option_config_json)
    # tvshow xml downloader and general api interface
    THETVDB_API = common_metadata_thetvdb.CommonMetadataTheTVDB(option_config_json)
else:
    THETVDB_CONNECTION = None


# setup the tvmaze class
if option_config_json['API']['tvmaze'] is not None:
    TVMAZE_CONNECTION = common_metadata_tvmaze.CommonMetadatatvmaze(option_config_json)
else:
    TVMAZE_CONNECTION = None


def tv_search_tvmaze(db_connection, file_name, lang_code='en'):
    """
    # tvmaze search
    """
    logging.info("meta tv search tvmaze: %s", file_name)
    file_name = guessit(file_name)
    metadata_uuid = None
    tvmaze_id = None
    if TVMAZE_CONNECTION is not None:
        if 'year' in file_name:
            tvmaze_id = str(TVMAZE_CONNECTION.com_thetvdb_search(file_name['title'],\
                file_name['year'], lang_code, True))
        else:
            tvmaze_id = str(TVMAZE_CONNECTION.com_thetvdb_search(file_name['title'],\
                None, lang_code, True))
        logging.info("response: %s", tvmaze_id)
        if tvmaze_id is not None:
#            # since there has been NO match whatsoever.....can "wipe" out everything
#            media_id_json = json.dumps({'tvmaze_id': tvmaze_id})
#            logging.info("dbjson: %s", media_id_json)
            # check to see if metadata exists for tvmaze id
            metadata_uuid = db_connection.db_metatv_guid_by_tvmaze(tvmaze_id)
            logging.info("db result: %s", metadata_uuid)
    logging.info('meta tv uuid %s prov id: %s', metadata_uuid, tvmaze_id)
    return metadata_uuid, tvmaze_id


def tv_search_tvdb(db_connection, file_name, lang_code='en'):
    """
    # tvdb search
    """
    logging.info("meta tv search tvdb: %s", file_name)
    file_name = guessit(file_name)
    metadata_uuid = None
    tvdb_id = None
    if THETVDB_CONNECTION is not None:
        if 'year' in file_name:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],\
                file_name['year'], lang_code, True))
        else:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],\
                None, lang_code, True))
        logging.info("response: %s", tvdb_id)
        if tvdb_id is not None:
#            # since there has been NO match whatsoever.....can "wipe" out everything
#            media_id_json = json.dumps({'thetvdb': tvdb_id})
#            logging.info("dbjson: %s", media_id_json)
            # check to see if metadata exists for TVDB id
            metadata_uuid = db_connection.db_metatv_guid_by_tvdb(tvdb_id)
            logging.info("db result: %s", metadata_uuid)
    logging.info('meta tv uuid %s prov id: %s', metadata_uuid, tvdb_id)
    return metadata_uuid, tvdb_id


def tv_fetch_save_tvdb(db_connection, tvdb_id):
    """
    # tvdb data fetch
    """
    logging.info("meta tv tvdb save fetch: %s", tvdb_id)
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


def tv_fetch_save_tvmaze(db_connection, tvmaze_id):
    """
    Fetch show data from tvmaze
    """
    logging.info("meta tv tvmaze save fetch: %s", tvmaze_id)
    metadata_uuid = None
    #show_full_json = tvmaze.com_meta_TheMaze_Show_by_ID(tvmaze_id, None, None, None, True)
    show_full_json = None
    try:
        show_full_json = ({'Meta': {'tvmaze':\
            json.loads(common_metadata_tvmaze.com_meta_tvmaze_show_by_id(\
            tvmaze_id, None, None, None, True))}})
    except:
        pass
    logging.info("tvmaze full: %s", show_full_json)
    if show_full_json is not None:
#        for show_detail in show_full_json:
        show_detail = show_full_json['Meta']['tvmaze']
        logging.info("detail: %s", show_detail)
        tvmaze_name = show_detail['name']
        logging.info("name: %s", tvmaze_name)
        try:
            tvrage_id = str(show_detail['externals']['tvrage'])
        except:
            tvrage_id = None
        try:
            thetvdb_id = str(show_detail['externals']['thetvdb'])
        except:
            thetvdb_id = None
        try:
            imdb_id = str(show_detail['externals']['imdb'])
        except:
            imdb_id = None
        series_id_json = json.dumps({'tvmaze': str(tvmaze_id), 'TVRage': tvrage_id,\
            'imdb': imdb_id, 'thetvdb': thetvdb_id})
        image_json = {'Images': {'tvmaze': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
        metadata_uuid = db_connection.db_meta_tvmaze_insert(series_id_json, tvmaze_name,\
            json.dumps(show_full_json), json.dumps(image_json))
        # store person info
        if 'cast' in show_full_json['Meta']['tvmaze']['_embedded']:
            db_connection.db_meta_person_insert_cast_crew('tvmaze',\
                show_full_json['Meta']['tvmaze']['_embedded']['cast'])
        if 'crew' in show_full_json['Meta']['tvmaze']['_embedded']:
            db_connection.db_meta_person_insert_cast_crew('tvmaze',\
                show_full_json['Meta']['tvmaze']['_embedded']['crew'])
        db_connection.db_commit()
    return metadata_uuid


def metadata_tv_lookup(db_connection, media_file_path, download_que_json, download_que_id,\
                       file_name):
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
        metadata_tv_lookup.metadata_last_rt = None
    metadata_uuid = None # so not found checks verify later
    logging.info('tvlook filename: %s', file_name)
    # check for dupes by name/year
    if 'year' in file_name:
        logging.info('tv here 1')
        if file_name['title'] == metadata_tv_lookup.metadata_last_title\
                and file_name['year'] == metadata_tv_lookup.metadata_last_year:
            logging.info('tv here 2')
            db_connection.db_download_delete(download_que_id)
            logging.info('meta tv return 1 %s',  metadata_tv_lookup.metadata_last_id)
            return metadata_tv_lookup.metadata_last_id
    elif file_name['title'] == metadata_tv_lookup.metadata_last_title:
        logging.info('tv here 3')
        db_connection.db_download_delete(download_que_id)
        logging.info('meta tv return 2 %s',  metadata_tv_lookup.metadata_last_id)
        return metadata_tv_lookup.metadata_last_id
    logging.info('tv before nfo/xml')
    # grab by nfo/xml data
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file_tv(media_file_path)
    imdb_id, tvdb_id, rt_id = metadata_nfo_xml.nfo_xml_id_lookup_tv(nfo_data, xml_data)
    logging.info("tv look: %s %s %s", imdb_id, tvdb_id, rt_id)
    # if same as last, return last id and save lookup
    # check these dupes as the nfo/xml files might not exist to pull the metadata id from
    if imdb_id is not None and imdb_id == metadata_tv_lookup.metadata_last_imdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    if tvdb_id is not None and tvdb_id == metadata_tv_lookup.metadata_last_tvdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    if rt_id is not None and rt_id == metadata_tv_lookup.metadata_last_rt:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    # if ids from nfo/xml, query local db to see if exist
    if tvdb_id is not None:
        metadata_uuid = db_connection.db_metatv_guid_by_tvdb(tvdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_metatv_guid_by_imdb(imdb_id)
    if rt_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_metatv_guid_by_rt(rt_id)
    # if ids from nfo/xml on local db
    logging.info("meta tv metadata_uuid A: %s", metadata_uuid)
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last name/year id's
    else:
        # id is known from nfo/xml but not in db yet so fetch data
        if tvdb_id is not None or imdb_id is not None:
            if tvdb_id is not None:
                dl_meta = db_connection.db_download_que_exists(download_que_id,\
                                                               'thetvdb', str(tvdb_id))
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(tvdb_id)})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('thetvdb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
            else:
                dl_meta = db_connection.db_download_que_exists(download_que_id,\
                    'thetvdb', imdb_id)
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': imdb_id})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('thetvdb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
    logging.info("meta tv metadata_uuid B: %s", metadata_uuid)
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        logging.info("tv db lookup")
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(file_name['title'],\
                file_name['year'])
        else:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(file_name['title'], None)
        logging.info("tv db meta: %s", metadata_uuid)
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            # no matches by name/year
            # search tvmaze since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),\
                download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('tvmaze', download_que_id)
    # set last values to negate lookups for same show
    metadata_tv_lookup.metadata_last_id = metadata_uuid
    metadata_tv_lookup.metadata_last_title = file_name['title']
    try:
        metadata_tv_lookup.metadata_last_year = file_name['year']
    except:
        metadata_tv_lookup.metadata_last_year = None
    metadata_tv_lookup.metadata_last_imdb = imdb_id
    metadata_tv_lookup.metadata_last_tvdb = tvdb_id
    metadata_tv_lookup.metadata_last_rt = rt_id
    return metadata_uuid
