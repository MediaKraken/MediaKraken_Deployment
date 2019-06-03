'''
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
from common import common_global

from . import metadata_nfo_xml


def metadata_adult_lookup(db_connection, download_que_json, download_que_id, file_name):
    """
    Adult lookup
    This is the main function called from metadata_identification
    """
    # don't bother checking title/year as the main_server_metadata_api_worker does it already
    if not hasattr(metadata_adult_lookup, "metadata_last_id"):
        # it doesn't exist yet, so initialize it
        metadata_adult_lookup.metadata_last_id = None
        metadata_adult_lookup.metadata_last_imdb = None
        metadata_adult_lookup.metadata_last_tmdb = None
    metadata_uuid = None  # so not found checks verify later
    common_global.es_inst.com_elastic_index('info', {'metadata_adult_lookup': str(file_name)})
    # determine provider id's from nfo/xml if they exist
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file(download_que_json['Path'])
    imdb_id, tmdb_id, rt_id = metadata_nfo_xml.nfo_xml_id_lookup(nfo_data, xml_data)
    if imdb_id is not None or tmdb_id is not None or rt_id is not None:
        common_global.es_inst.com_elastic_index('info', {"meta adult look": imdb_id,
                                                         'tmdb': tmdb_id,
                                                         'rt': rt_id})
    # if same as last, return last id and save lookup
    if imdb_id is not None and imdb_id == metadata_adult_lookup.metadata_last_imdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_adult_lookup.metadata_last_id
    if tmdb_id is not None and tmdb_id == metadata_adult_lookup.metadata_last_tmdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_adult_lookup.metadata_last_id
    # doesn't match last id's so continue lookup
    # if ids from nfo/xml, query local db to see if exist
    if tmdb_id is not None:
        metadata_uuid = db_connection.db_meta_guid_by_tmdb(tmdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_imdb(imdb_id)
    # if ids from nfo/xml on local db
    common_global.es_inst.com_elastic_index('info', {"meta adult metadata_uuid A": metadata_uuid})
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last id's
    else:
        # check to see if id is known from nfo/xml but not in db yet so fetch data
        if tmdb_id is not None or imdb_id is not None:
            if tmdb_id is not None:
                provider_id = str(tmdb_id)
            else:
                provider_id = imdb_id
            dl_meta = db_connection.db_download_que_exists(download_que_id, 1, 'pornhub',
                                                           provider_id)
            if dl_meta is None:
                metadata_uuid = download_que_json['MetaNewID']
                download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': provider_id})
                db_connection.db_download_update(json.dumps(download_que_json),
                                                 download_que_id)
                # set provider last so it's not picked up by the wrong thread too early
                db_connection.db_download_update_provider('pornhub', download_que_id)
            else:
                db_connection.db_download_delete(download_que_id)
                metadata_uuid = dl_meta
    common_global.es_inst.com_elastic_index('info', {"meta adult metadata_uuid B": metadata_uuid})
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        common_global.es_inst.com_elastic_index('info', {'stuff': "meta adult db lookup"})
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'],
                                                                file_name['year'])
        else:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'], None)
        common_global.es_inst.com_elastic_index('info', {"meta adult db meta": metadata_uuid})
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            metadata_uuid = download_que_json['MetaNewID']
            # no matches by name/year on local database
            # search themoviedb since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),
                                             download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('pornhub', download_que_id)
    common_global.es_inst.com_elastic_index('info', {"metadata_adult return uuid": metadata_uuid})
    # set last values to negate lookups for same title/show
    metadata_adult_lookup.metadata_last_id = metadata_uuid
    metadata_adult_lookup.metadata_last_imdb = imdb_id
    metadata_adult_lookup.metadata_last_tmdb = tmdb_id
    return metadata_uuid