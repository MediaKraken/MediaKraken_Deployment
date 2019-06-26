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

import json
import os

from common import common_config_ini
from common import common_global
from common import common_metadata
from common import common_metadata_provider_isbndb

option_config_json, db_connection = common_config_ini.com_config_read()

if option_config_json['API']['isbndb'] is not None:
    # setup the isbndb class
    ISBNDB_CONNECTION = common_metadata_provider_isbndb.CommonMetadataISBNdb(
        option_config_json)
else:
    ISBNDB_CONNECTION = None


def metadata_periodicals_search_isbndb(db_connection, lookup_name):
    """
    search isbndb
    """
    common_global.es_inst.com_elastic_index('info', {"meta book search isbndb": lookup_name})
    metadata_uuid = None
    match_result = None
    common_global.es_inst.com_elastic_index('info', {'wh': ISBNDB_CONNECTION})
    if ISBNDB_CONNECTION is not None:
        api_response = ISBNDB_CONNECTION.com_isbndb_books(lookup_name)
        common_global.es_inst.com_elastic_index('info', {'response': api_response})
        if api_response.status_code == 200:
            # TODO verify decent results before insert
            common_global.es_inst.com_elastic_index('info', {'resp json': api_response.json()})
            if 'error' in api_response.json():
                common_global.es_inst.com_elastic_index('info', {'stuff': 'error skipp'})
            else:
                metadata_uuid = db_connection.db_meta_book_insert(
                    api_response.json())
    common_global.es_inst.com_elastic_index('info', {'meta book uuid': metadata_uuid,
                                                     'result': match_result})
    return metadata_uuid, match_result


def metadata_periodicals_lookup(db_connection, download_que_json, download_que_id):
    """
    Lookup via isbn and then name
    """
    metadata_uuid = None  # so not found checks verify later
    # check if isbn in metaid
    if download_que_json['ProviderMetaID'] is not None:
        # check local database
        metadata_uuid = db_connection.db_meta_book_guid_by_isbn(
            download_que_json['ProviderMetaID'], download_que_json['ProviderMetaID'])
    else:
        # try to pull isbn out..might not be long enough, so try
        try:
            metadata_uuid = db_connection.db_meta_book_guid_by_isbn(download_que_json['Path'][-10:],
                                                                    download_que_json['Path'][-13:])
        except:
            pass
    if metadata_uuid is None:
        if download_que_json['ProviderMetaID'] is None:
            lookup_name = os.path.basename(
                os.path.splitext(download_que_json['Path'])[0]).replace('_', ' ')
            metadata_uuid = db_connection.db_meta_book_guid_by_name(lookup_name)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),
                                             download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider(
                'isbndb', download_que_id)
    else:
        # meta uuid is found so delete
        db_connection.db_download_delete(download_que_id)
    return metadata_uuid


def metadata_periodicals_cover(db_connection, isbn):
    """
    pull and save the cover image for periodical
    """
    # TODO use the cover pull in common_metadata_open_library
    url = ('http://covers.openlibrary.org/b/ISBN/%s-L.jpg?default=false', isbn)

    common_metadata.com_meta_image_path(download_data['Name'],
                                        'poster', 'themoviedb', download_data['Poster'])

    return False
