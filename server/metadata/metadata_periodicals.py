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

import os
import logging
import sys
sys.path.append("../common")
import MK_Common_ISBNdb
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")


if Config.get('API', 'ISBNdb').strip() != 'None':
    # setup the isbndb class
    ISBNdb_API_Connection = MK_Common_ISBNdb.MK_Common_ISBNdb_API()
else:
    ISBNdb_API_Connection = None


def metadata_periodicals_lookup(db, media_file_path, download_que_id):
    metadata_uuid = None
    # try to pull isbn out..might not be long enough, so try
    try:
        metadata_uuid = db.MK_Server_Database_MetadataBook_GUID_By_ISBN(media_file_path[-10:], media_file_path[-13:])
    except:
        pass
    if metadata_uuid is None:
        lookup_name = os.path.basename(os.path.splitext(media_file_path)[0]).replace('_',' ')
        metadata_uuid = db.MK_Server_Database_MetadataBook_GUID_By_Name(lookup_name)
        if metadata_uuid is None and ISBNdb_API_Connection is not None:
            json_data = ISBNdb_API_Connection.MK_Common_ISBNdb_Books(lookup_name)
            if json_data is None or 'error' in json_data:
                logging.error("isbn book error: %s", json_data)
            else:
                # TODO verify decent results before insert
                metadata_uuid = db.MK_Server_Database_MetadataBook_Book_Insert(json_data)
    return metadata_uuid