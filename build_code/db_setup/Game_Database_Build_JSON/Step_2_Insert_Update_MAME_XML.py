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
import xmltodict
# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
conn = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
curs = conn.cursor()

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

# create mame game list
print("begin parse")
found_game = 0
update_game = 0
insert_game = 0
with open("mame.xml", 'r') as xml_file:
    print("after open")
    json_data = xmltodict.parse(xml_file.read())
    print("after json")
    #json_data = json.load(xml_data)
    for child_of_root in json_data['mame']['machine']:
        found_game += 1
        print("child: %s", child_of_root)
        # see if exists then need to update
        quick_sql_args = child_of_root['@name'],
        curs.execute('select count(*) from mm_metadata_game_systems_info where gs_game_system_json->\'@name\' ? %s', quick_sql_args)
        if int(curs.fetchone()[0]) > 0:
            sql_args = json.dumps(child_of_root), child_of_root['@name']
            #curs.execute('update mm_metadata_game_systems_info set gs_game_system_json = %s where gs_game_system_json->\'@name\' ? %s',sql_args)
            update_game += 1
        else:
            row_id = str(uuid.uuid4())
            sql_args = row_id, json.dumps(child_of_root)
            curs.execute('insert into mm_metadata_game_systems_info (gs_id, gs_game_system_json) values (%s,%s)', sql_args)
            insert_game += 1
        print("found: %s", found_game)

print("total: %s", found_game)
print("update: %s", update_game)
print("insert: %s", insert_game)

# close db files
conn.commit()
conn.close()
