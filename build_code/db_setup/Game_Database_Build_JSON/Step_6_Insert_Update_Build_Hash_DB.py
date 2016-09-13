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
import uuid
import psycopg2
import json
import os
import xmltodict
# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
conn = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
curs = conn.cursor()


total_software = 0
path = "./hash"
dirList = os.listdir(path)
for fname in dirList:
    print("fname: %s", fname)
    sys_id_to_store = None
    # find system id from mess
    file_name, ext = os.path.splitext(fname)
    # file_name needs to _flop, _cart etc cut off
    # can't do this as some systems have a _ in the name - file_name = file_name.rsplit("_",1)[0]
    file_name = file_name.replace("_cd", "").replace("_cart", "").replace("_cass", "").replace("_flop", "").replace("_rom", "").replace("_disk", "").replace("_hdd", "")
    if ext == ".xml":
        sql_args = file_name.replace(".xml", ""),
        curs.execute('select gs_id from mm_metadata_game_systems_info'\
            ' where gs_game_system_json->\'@name\' ? %s', sql_args)
        row_data = curs.fetchone()
        if row_data is not None:
            sys_id_to_store = row_data[0]
            #with open("mame.xml", 'r') as xml_file:
                #json_data = xmltodict.parse(xml_file.read())
            with open(os.path.join(path, fname), 'r') as data_file:
                #json_file = json.load(data_file)
                json_file = xmltodict.parse(data_file.read())
                for json_game in json_file['softwarelist']['software']:
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    row_id = str(uuid.uuid4())
                    sql_args = row_id, sys_id_to_store, json.dumps(json_game)
                    curs.execute('insert into mm_metadata_game_software_info (gi_id,'\
                        ' gi_system_id, gi_game_info_json) values (%s,%s,%s)', sql_args)
                    total_software += 1
        else:
            print("system not found: %s", sql_args[0])
            # TODO add "new" system
    elif ext == ".hsi":
        sql_args = file_name.replace(".hsi", ""),
        curs.execute('select gs_id from mm_metadata_game_systems_info'\
            ' where gs_game_system_json->\'@name\' ? %s', sql_args)
        row_data = curs.fetchone()
        if row_data is not None:
            sys_id_to_store = row_data[0]
            #with open("mame.xml", 'r') as xml_file:
                #json_data = xmltodict.parse(xml_file.read())
            with open(os.path.join(path, fname), 'r') as data_file:
                #json_file = json.load(data_file)
                json_file = xmltodict.parse(data_file.read())
                for json_game in json_file['hashfile']['hash']:
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    row_id = str(uuid.uuid4())
                    sql_args = row_id, sys_id_to_store, json.dumps(json_game)
                    curs.execute("insert into mm_metadata_game_software_info (gi_id,'\
                        ' gi_system_id, gi_game_info_json) values (%s,%s,%s)", sql_args)
                    total_software += 1
        else:
            print("system not found: %s", sql_args[0])
            # TODO add "new" system



print("total: %s", total_software)
# close db files
conn.commit()
conn.close()
