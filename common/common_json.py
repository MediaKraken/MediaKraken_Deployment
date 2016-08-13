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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import glob
import json
from kivy import platform
from common import common_database_octmote


def com_json_find():
    """
    Check for new json files for device/layout/etc
    """
    if platform == 'android':
        file_path = '/mnt/extsd/OctMote_Json/'
    else:
        file_path = './OctMote_Json/'
    for file_name in glob.glob(file_path + "*.txt"):
        logging.debug(file_name)
        com_json_import(file_name)


def com_json_import(file_name):
    """
    Import new jsons into database or update them if found
    """
    logging.debug("json import: %s", file_name)
    file_handle = open(file_name, 'r')
    json_data = file_handle.read()
    file_handle.close()
    try:
        # item type
        common_database_octmote.MK_Database_Sqlite3_Item_Insert(json_data)
    except:
        try:
            # layout
            common_database_octmote.MK_Database_Sqlite3_Layout_Config_Insert(json_data['Layout'],\
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
