"""
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
"""

import inspect
import os

from common import common_logging_elasticsearch_httpx
from common import common_metadata


async def metadata_periodicals_lookup(db_connection, download_data):
    """
    Lookup via isbn and then name
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    metadata_uuid = None  # so not found checks verify later
    # check if isbn in metaid
    if download_data['ProviderMetaID'] is not None:
        # check local database
        metadata_uuid = db_connection.db_meta_book_guid_by_isbn(
            download_data['ProviderMetaID'], download_data['ProviderMetaID'])
    else:
        # try to pull isbn out..might not be long enough, so try
        try:
            metadata_uuid = db_connection.db_meta_book_guid_by_isbn(download_data['Path'][-10:],
                                                                    download_data['Path'][-13:])
        except:
            pass
    if metadata_uuid is None:
        if download_data['ProviderMetaID'] is None:
            lookup_name = os.path.basename(
                os.path.splitext(download_data['Path'])[0]).replace('_', ' ')
            metadata_uuid = db_connection.db_meta_book_guid_by_name(lookup_name)
        if metadata_uuid is None:
            download_data.update({'Status': 'Search'})
            # save the updated status
            await db_connection.db_begin()
            await db_connection.db_download_update(download_data,
                                                   download_que_id)
            # set provider last so it's not picked up by the wrong thread
            await db_connection.db_download_update_provider(
                'isbndb', download_que_id)
            await db_connection.db_commit()
    else:
        # meta uuid is found so delete
        await db_connection.db_download_delete(download_que_id)
        await db_connection.db_commit()
    return metadata_uuid


async def metadata_periodicals_cover(db_connection, isbn):
    """
    pull and save the cover image for periodical
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    # TODO use the cover pull in common_metadata_open_library
    url = ('http://covers.openlibrary.org/b/ISBN/%s-L.jpg?default=false', isbn)

    common_metadata.com_meta_image_path(download_data['Name'],
                                        'poster', 'themoviedb', download_data['Poster'])

    return False
