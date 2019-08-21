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

import json
import os

from common import common_metadata


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
