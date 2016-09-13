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
import chardet
import sys
import psycopg2
import json
import uuid
sys.path.append("../../common")
from common import common_file

# functions to deal with database data
sql3_conn = None
sql3_cursor = None

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn\
    = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()
sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class WHERE relname = 'mm_media'")
if sql3_cursor.fetchone()[0] > 0:
    # file all dictid files
    for dict_data in common_file.com_file_Dir_List('/home/spoot/nfsmount/SQL_Dump/FreeDB',\
            None, True, False):
        file_pointer = open(dict_data, "r").read()
        result = chardet.detect(file_pointer)
        charenc = result['encoding']
        try:
            sql_params = str(uuid.uuid4()), dict_data.rsplit('/', 1)[1],\
                json.dumps({'discid_data':file_pointer.decode(charenc).encode('utf-8')})
            sql3_cursor.execute('insert into mm_discid (mm_discid_guid, mm_discid_discid,'\
                ' mm_discid_media_info) values (%s,%s,%s)', sql_params)
            print("insert: %s", dict_data)
        except:
            print("skipping: %s", dict_data)
        #file_pointer.close()    # TODO why is this commented out?

# commit and close
sql3_conn.commit()
sql3_conn.close()
