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
import psycopg2
import json
# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
conn = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
curs = conn.cursor()

game_titles = []
game_desc = ""
add_to_desc = False
history_file = open("history.dat", "rb")
while 1:
    line = history_file.readline()
    if not line:
        break
    if line.find("$info=") == 0:
        game_titles = line.split("=", 1)[1].split(",")
    elif line.find("$end") == 0:
        add_to_desc = False
        for game in game_titles:
            sql_params = game
            curs.execute('select gi_game_info_json from mm_game_info where gi_game_info_json->\'@name\' ? %s', sql_params)
            json_data = json.loads(curs.fetchone()[0])
            json_data['overview'] = game_desc
            sql_args = json.dumps(json_data), game
            curs.execute("update mm_game_info set gi_game_info_json = %s where gi_game_info_json->\'@name\' ? %s", sql_args)
            game_desc = ""
    if add_to_desc:
        game_desc += line
    if line.find("$bio") == 0:
        add_to_desc = True
history_file.close()
# close db files
conn.commit()
conn.close()
