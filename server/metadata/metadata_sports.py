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
import json
import sys
sys.path.append("../common")
from common import common_metadata_thesportsdb
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")


# verify thesportsdb key exists
if Config.get('API', 'thesportsdb').strip() != 'None':
    thesportsdb_API_Connection = common_metadata_thesportsdb.com_meta_thesportsdb_API()
else:
    thesportsdb_API_Connection = None


def metadata_sports_lookup(db, media_file_path, download_que_id):
    """
    Lookup sporting event by name
    """
    stripped_name = os.path.basename(media_file_path.replace('_', ' ').rsplit('(', 1)[0].strip())
    metadata_uuid = db.srv_db_meta_sports_guid_by_event_name(stripped_name)
    if metadata_uuid is None and thesportsdb_API_Connection is not None:
        logging.debug("searching: %s", stripped_name)
        thesportsdb_data = thesportsdb_API_Connection.com_meta_thesportsdb_Search_Event_by_Name(stripped_name)
        logging.debug("sports return: %s", thesportsdb_data)
        # "valid" key returned in case of null response........or event none
        if thesportsdb_data is not None:
            thesportsdb_data = json.loads(thesportsdb_data)
            if thesportsdb_data['event'] is not None:
                # TODO "find" the rigth event by name?  if multiples?
                metadata_uuid = db.srv_db_metaSports_GUID_by_thesportsdb(\
                    thesportsdb_data['event'][0]['idEvent'])
                if metadata_uuid is None:
                    image_json = {'Images': {'thesportsdb': {'Characters': {}, 'Banner': None,\
                        'Poster': None, 'Backdrop': None, "Redo": True}}}
                    media_id_json = json.dumps({'thesportsdb':\
                        str(thesportsdb_data['event'][0]['idEvent'])})
                    db.srv_db_metathesportsdb_Insert(media_id_json,\
                        thesportsdb_data['event'][0]['strFilename'], json.dumps(thesportsdb_data),\
                        json.dumps(image_json))
    return metadata_uuid
