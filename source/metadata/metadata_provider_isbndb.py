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

from common import common_config_ini
from common import common_global
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
