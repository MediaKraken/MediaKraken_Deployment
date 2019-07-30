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
from common import common_metadata_provider_thesportsdb

option_config_json, db_connection = common_config_ini.com_config_read()

# verify thesportsdb key exists
if option_config_json['API']['thesportsdb'] is not None:
    THESPORTSDB_CONNECTION \
        = common_metadata_provider_thesportsdb.CommonMetadataTheSportsDB(option_config_json)
else:
    THESPORTSDB_CONNECTION = None
