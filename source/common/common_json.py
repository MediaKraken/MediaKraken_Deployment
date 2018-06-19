'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

import glob
import json

from kivy import platform

from . import common_database_octmote
from . import common_global


def com_json_find():
    """
    Check for new json files for device/layout/etc
    """
    if platform == 'android':
        file_path = '/mnt/extsd/OctMote_Json/'
    else:
        file_path = './OctMote_Json/'
    for file_name in glob.glob(file_path + "*.txt"):
        common_global.es_inst.com_elastic_index('info', {'stuff': file_name})
        com_json_import(file_name)


def com_json_import(file_name):
    """
    Import new jsons into database or update them if found
    """
    common_global.es_inst.com_elastic_index('info', {"json import": file_name})
    file_handle = open(file_name, 'r')
    json_data = file_handle.read()
    file_handle.close()
    try:
        # item type
        common_database_octmote.com_db_item_insert(json_data)
    except:
        try:
            # layout
            common_database_octmote.com_db_layout_config_insert(json_data['Layout'],
                                                                json_data)
        except:
            pass


def com_json_load_file(file_name):
    """
    Load file as json data
    """
    file_handle = open(file_name, 'r')
    json_data = json.loads(file_handle.read())
    file_handle.close()
    return json_data
