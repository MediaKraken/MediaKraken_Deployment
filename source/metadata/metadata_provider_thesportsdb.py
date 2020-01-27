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

from common import common_config_ini
from common import common_global
from common import common_metadata_provider_thesportsdb

option_config_json, db_connection = common_config_ini.com_config_read()

THESPORTSDB_CONNECTION \
    = common_metadata_provider_thesportsdb.CommonMetadataTheSportsDB(option_config_json)

def search_thesportsdb(db_connection, file_name):
    """
    # search thesportsdb
    """
    try:
        common_global.es_inst.com_elastic_index('info', {"meta movie search thesportsdb": str(file_name)})
    except:
        pass

    common_global.es_inst.com_elastic_index('info', {'search_thesportsdb': str(file_name)})


    common_global.es_inst.com_elastic_index('info', {'meta thesportsdb uuid': metadata_uuid,
                                                     'result': match_result})
    return metadata_uuid, match_result
