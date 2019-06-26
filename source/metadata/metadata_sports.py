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
from common import common_metadata_provider_thesportsdb

option_config_json, db_connection = common_config_ini.com_config_read()

# verify thesportsdb key exists
if option_config_json['API']['thesportsdb'] is not None:
    THESPORTSDB_CONNECTION \
        = common_metadata_provider_thesportsdb.CommonMetadataTheSportsDB(option_config_json)
else:
    THESPORTSDB_CONNECTION = None


def metadata_sports_lookup(db_connection, download_data, download_que_id):
    """
    Lookup sporting event by name
    """
    stripped_name = os.path.basename(
        download_data['mdq_download_json']['Path'].replace('_', ' ').rsplit('(', 1)[0].strip())
    metadata_uuid = db_connection.db_meta_sports_guid_by_event_name(stripped_name)
    if metadata_uuid is None and THESPORTSDB_CONNECTION is not None:
        common_global.es_inst.com_elastic_index('info', {"searching": stripped_name})
        thesportsdb_data = \
            THESPORTSDB_CONNECTION.com_meta_thesportsdb_search_event_by_name(stripped_name)
        common_global.es_inst.com_elastic_index('info', {"sports return": thesportsdb_data})
        # "valid" key returned in case of null response........or event none
        if thesportsdb_data is not None:
            thesportsdb_data = json.loads(thesportsdb_data)
            if thesportsdb_data['event'] is not None:
                # TODO "find" the right event by name?  if multiples?
                metadata_uuid = db_connection.db_meta_sports_guid_by_thesportsdb(
                    thesportsdb_data['event'][0]['idEvent'])
                if metadata_uuid is None:
                    image_json = {'Images': {'thesportsdb': {'Characters': {}, 'Banner': None,
                                                             'Poster': None, 'Backdrop': None,
                                                             "Redo": True}}}
                    media_id_json = json.dumps({'thesportsdb':
                                                    str(thesportsdb_data['event'][0]['idEvent'])})
                    db_connection.db_metathesportsdb_insert(media_id_json,
                                                            thesportsdb_data['event'][0][
                                                                'strFilename'],
                                                            json.dumps(
                                                                thesportsdb_data),
                                                            json.dumps(image_json))
                    db_connection.db_download_delete(download_que_id)
    return metadata_uuid
