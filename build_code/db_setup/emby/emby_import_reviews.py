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
import os
import sys
import uuid
import psycopg2
import json
sys.path.append("../../../common")
from common import common_database_emby
from common import common_emby
from common import common_file

# import localization
import locale
locale.setlocale(locale.LC_ALL, '')

# functions to deal with database data
sql3_conn = None
sql3_cursor = None

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn\
     = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()

# open emby
common_database_emby.com_db_open_emby('/home/spoot/nfsmount/SQL_Dump/data/library.db')

added_record = 0
skipped_record = 0
for review_json in common_file.com_file_dir_list(\
        '/home/spoot/nfsmount/SQL_Dump/emby_data/critic-reviews/', None, None, False):
    print("File: %s", review_json)
    with open(review_json) as data_file:
        json_data = json.load(data_file)
        # determine emby/metadata guid from file name uuid
        header, emby_guid = os.path.split(review_json)
        emby_c_guid = common_emby.com_emby_uuid_to_guid(emby_guid.split('.', 1)[0])
        emby_data = common_database_emby.com_db_media_by_guid(emby_c_guid)
        if emby_data is not None:
            # emby_data[0] is the C# id

            #metadata_guid = lookupondb via guid.....take imdb lookup metadataid

            # loop through reviews and insert or skip if exists
            for json_block in json_data:
                # check to see if review exists
                sql_params = metadata_guid, json.dumps(json_block)
                sql3_cursor.execute('select count(*) from mm_review'\
                    ' where mm_review_metadata_guid = %s and mm_review_json = %s', sql_params)
                if sql3_cursor.fetchone()[0] > 0:
                    skipped_record += 1
                else:
                    sql_params = str(uuid.uuid4()), metadata_guid, json.dumps(json_block)
                    sql3_cursor.execute('insert into mm_review (mm_review_guid,'\
                        ' mm_review_metadata_guid, mm_review_json) values (%s,%s,%s)', sql_params)
                    added_record += 1

# close emby
common_database_emby.com_db_close_emby()
# commit and close
sql3_conn.commit()
sql3_conn.close()

# print totals
print("Imported: %s", locale.format('%d', added_record, True))
print("Skipped: %s", locale.format('%d', skipped_record, True))
