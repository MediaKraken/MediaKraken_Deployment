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

import uuid

import psycopg2

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
conn = psycopg2.connect(
    "dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
curs = conn.cursor()

infile = open("messinfo.dat", "r")
start_system_read = False
skip_next_line = False
long_name_next = False
desc_next = False
wip_in_progress = False
romset_in_progress = False
# store args to sql
sys_shortname = ""
sys_longname = None
sys_manufacturer = None
sys_year = None
sys_desc = None
sys_emulation = None
sys_color = None
sys_sound = None
sys_graphics = None
sys_save_state = None
sys_wip = ""
sys_romset = None

sql_string = ""
line_count = 0
while 1:
    line_count += 1
    line = infile.readline()
    if not line:
        break
    if skip_next_line:
        skip_next_line = False
    else:
        if line.find("DRIVERS INFO") != -1:  # stop at drivers
            break
        line = line.replace("    ", "")
        if line[0] == "#" or len(line) < 4 or line.find(
                "$mame") == 0:  # skip comments and blank lines
            if line.find("$mame") == 0:
                skip_next_line = True
                long_name_next = True
        elif line.find("$info") == 0:  # found so begin start system read
            start_system_read = True
            # load the short name
            sys_short_name = line.split('=')[1]
        elif line.find("Emulation:") == 0:  # found so begin start system read
            sys_emulation = line.split(' ')[1]
        elif line.find("Color:") == 0:  # found so begin start system read
            sys_color = line.split(' ')[1]
        elif line.find("Sound:") == 0:  # found so begin start system read
            sys_sound = line.split(' ')[1]
        elif line.find("Graphics:") == 0:  # found so begin start system read
            sys_graphics = line.split(' ')[1]
        elif line.find("Save State:") == 0:  # found so begin start system read
            if line.rsplit(' ', 1)[1][:-1] == "Supported":
                sys_save_state = True
            else:
                sys_save_state = False
        elif line.find("WIP:") == 0:  # found so begin start system read
            wip_in_progress = True
        elif line.find("Romset:") == 0:  # found so begin start system read
            wip_in_progress = False
            romset_in_progress = True
        else:
            if wip_in_progress and line.find("Romset:") != 0:
                # sys_wip += line[:-1] + "<BR>"
                pass
            if romset_in_progress and line.find("$end") != 0:
                # sys_romset += line[:-1] + "<BR>"
                pass
            if desc_next:
                sys_desc = line
                desc_next = False
            if long_name_next:
                try:
                    sys_longname, sys_manufacturer, sys_year = line.split(',')
                except:
                    sys_longname, msys_manufacturer, sys_year = line.rsplit(
                        ',', 2)
                long_name_next = False
                desc_next = True
            if line.find("$end") == 0:  # end of system info so store system into db
                romset_in_progress = False
                if sys_desc[:-1] == "...":
                    sys_desc = None
                else:
                    sys_desc = sys_desc[:-1]
                # lookup uuids
                sys_manufacturer = Manufacturer_Lookup_Add(sys_manufacturer)
                sys_emulation = Status_Lookup_Add(sys_emulation[:-1])
                sys_color = Status_Lookup_Add(sys_color[:-1])
                sys_sound = Status_Lookup_Add(sys_sound[:-1])
                sys_graphics = Status_Lookup_Add(sys_graphics[:-1])
                # build query
                sql_args = str(uuid.uuid4()), sys_short_name[:-1], sys_longname, sys_desc, \
                           sys_year[:-1], sys_manufacturer, sys_emulation, sys_color, sys_sound, \
                           sys_graphics, sys_save_state
                print(sql_args)
                quick_sql_args = sys_short_name[:-1],
                curs.execute('select count(*) from mm_game_systems_info'
                             ' where gs_game_system_json->\'@name\' ? %s', quick_sql_args)
                if int(curs.fetchone()[0]) > 0:
                    quick_sql_args = sys_desc, sys_short_name[:-1]
                    curs.execute('update mm_game_systems_info set gs_system_description = %s'
                                 ' where gs_game_system_json->\'@name\' ? %s', quick_sql_args)
                else:
                    str(uuid.uuid4())
                    curs.execute('insert into mm_game_systems_info (gs_id,gs_game_system_json)'
                                 ' values (%s,%s)', sql_args)
                sys_wip = None
                sys_romset = None
conn.commit()
conn.close()
