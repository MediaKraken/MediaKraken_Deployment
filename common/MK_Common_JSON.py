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
import logging
import json
from kivy import platform
import MK_Common_Database_Octmote


# check for new json files for device/layout/etc
def MK_Json_Find():
    if platform == 'android':
        file_path = '/mnt/extsd/OctMote_Json/'
    else:
        file_path = './OctMote_Json/'
    for file_name in glob.glob(file_path + "*.txt"):
        logging.debug(file_name)
        MK_Json_Import(file_name)


# import new jsons into database or update them if found
def MK_Json_Import(file_name):
    logging.debug("json import: %s", file_name)
    file_handle = open(file_name, 'r')
    json_data = file_handle.read()
    file_handle.close()
    try:
        # item type
        MK_Common_Database_Octmote.MK_Database_Sqlite3_Item_Insert(json_data)
    except:
        try:
            # layout
            MK_Common_Database_Octmote.MK_Database_Sqlite3_Layout_Config_Insert(json_data['Layout'], json_data)
        except:
            pass


# load file as json data
def MK_Json_Load_Json(file_name):
    file_handle = open(file_name, 'r')
    json_data = json.loads(file_handle.read())
    file_handle.close()
    return json_data
