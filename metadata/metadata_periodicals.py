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
import json
from common import common_config_ini
from common import common_network
from common import common_metadata_isbndb
option_config_json, db_connection = common_config_ini.com_config_read()


if option_config_json['API']['isbndb'] is not None:
    # setup the isbndb class
    ISBNDB_CONNECTION = common_metadata_isbndb.CommonMetadataISBNdb(option_config_json)
else:
    ISBNDB_CONNECTION = None


def metadata_periodicals_search_isbndb(db_connection, lookup_name):
    """
    search isbndb
    """
    logging.info("meta book search isbndb: %s", lookup_name)
    metadata_uuid = None
    match_result = None
    logging.info('wh %s', ISBNDB_CONNECTION)
    if ISBNDB_CONNECTION is not None:
        api_response = ISBNDB_CONNECTION.com_isbndb_books(lookup_name)
        logging.info('response %s', api_response)
        if api_response.status_code == 200:
            # TODO verify decent results before insert
            logging.info('resp json %s', api_response.json())
            if 'error' in api_response.json():
                logging.info('error skipp')
            else:
                metadata_uuid = db_connection.db_meta_book_insert(
                    api_response.json())
    logging.info('meta book uuid %s, result %s', metadata_uuid, match_result)
    return metadata_uuid, match_result


def metadata_periodicals_lookup(db_connection, media_file_path,
                                download_que_json, download_que_id):
    """
    Lookup via isbn and then name
    """
    metadata_uuid = None # so not found checks verify later
    # check if isbn in metaid
    if download_que_json['ProviderMetaID'] is not None:
        # check local database
        metadata_uuid = db_connection.db_meta_book_guid_by_isbn(
            download_que_json['ProviderMetaID'], download_que_json['ProviderMetaID'])
    else:
        # try to pull isbn out..might not be long enough, so try
        try:
            metadata_uuid = db_connection.db_meta_book_guid_by_isbn(media_file_path[-10:],
                media_file_path[-13:])
        except:
            pass
    if metadata_uuid is None:
        if download_que_json['ProviderMetaID'] is None:
            lookup_name = os.path.basename(os.path.splitext(media_file_path)[0]).replace('_', ' ')
            metadata_uuid = db_connection.db_meta_book_guid_by_name(lookup_name)
        if metadata_uuid is None:
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),
                download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('isbndb', download_que_id)
    else:
        # meta uuid is found so delete
        db_connection.db_download_delete(download_que_id)
    return metadata_uuid


def metadata_periodicals_cover(db_connection, isbn):
    """
    pull and save the cover image for periodical
    """
    url = ('http://covers.openlibrary.org/b/ISBN/%s-L.jpg?default=false', isbn)

    common_metadata.com_meta_image_path(download_data['Name'],
                                        'poster', 'themoviedb', download_data['Poster'])

    return False
