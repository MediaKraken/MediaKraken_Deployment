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
import sys
# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
conn = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
curs = conn.cursor()

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

'''
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
skip this program for now!!!!!!!!
'''
sys.exit()

# create mame game list
print("begin parse")
update_game = 0
insert_game = 0
total_game = 0
with open("softwarelist.json") as json_file:
    json_data = json.load(json_file)
    for child_of_root in json_data['softwarelists']['softwarelist']:
        print("child: %s", child_of_root)
        system_name = child_of_root['@name']
        sql_params = system_name,
        curs.execute('select gs_id from mm_metadata_game_systems_info'\
            ' where gs_game_system_json->\'@name\' ? %s', sql_params)
        row_data = curs.fetchone()
        if row_data is not None:
            for software_data in child_of_root['software']:
                total_game += 1
                print("software: %s %s", row_data[0], software_data)
                # see if exists then need to update
                quick_sql_args = software_data['@name'], row_data[0]
                curs.execute('select count(*) from mm_metadata_game_software_info'\
                    ' where gi_game_info_json->\'@name\' ? %s and gi_system_id = %s',\
                    quick_sql_args)
                if int(curs.fetchone()[0]) > 0:
                    sql_args = json.dumps(software_data), software_data['@name'], row_data[0]
                    curs.execute('update mm_metadata_game_software_info'\
                        ' set gi_game_info_json = %s where gi_game_info_json->\'@name\' ? %s'\
                        ' and gi_system_id = %s', sql_args)
                    update_game += 1
                else:
                    sql_args = str(uuid.uuid4()), row_data[0], json.dumps(software_data)
                    curs.execute('insert into mm_metadata_game_software_info (gi_id,'\
                        ' gi_system_id, gi_game_info_json) values (%s,%s,%s)', sql_args)
                    insert_game += 1

print("update: %s", update_game)
print("insert: %s", insert_game)
print("total game: %s", total_game)

# close db files
conn.commit()
conn.close()
