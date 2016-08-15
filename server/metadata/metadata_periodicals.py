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
import os
import sys
sys.path.append("../common")
from common import common_isbndb
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")


if Config.get('API', 'ISBNdb').strip() != 'None':
    # setup the isbndb class
    isbndb_api_connection = common_isbndb.com_ISBNdb_API()
else:
    isbndb_api_connection = None


def metadata_periodicals_lookup(db_connection, media_file_path, download_que_id):
    """
    Lookup via isdb and then name
    """
    metadata_uuid = None
    # try to pull isbn out..might not be long enough, so try
    try:
        metadata_uuid = db_connection.srv_db_metabook_guid_by_isbn(media_file_path[-10:],\
            media_file_path[-13:])
    except:
        pass
    if metadata_uuid is None:
        lookup_name = os.path.basename(os.path.splitext(media_file_path)[0]).replace('_', ' ')
        metadata_uuid = db_connection.srv_db_metabook_guid_by_name(lookup_name)
        if metadata_uuid is None and isbndb_api_connection is not None:
            json_data = isbndb_api_connection.com_ISBNdb_Books(lookup_name)
            if json_data is None or 'error' in json_data:
                logging.error("isbn book error: %s", json_data)
            else:
                # TODO verify decent results before insert
                metadata_uuid = db_connection.srv_db_metabook_book_insert(json_data)
    return metadata_uuid
