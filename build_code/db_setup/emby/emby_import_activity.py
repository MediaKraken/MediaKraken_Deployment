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
import sys
import psycopg2
import uuid
sys.path.append("../../../common")
from common import common_database_emby

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()

# open emby db
common_database_emby.com_db_open_emby('/home/spoot/nfsmount/SQL_Dump/emby_data/library.db',\
     attach_other_db=True)

# grab all activity data
for row_data in common_database_emby.com_db_emby_activity_list():
    sql_params = list(row_data)
    sql_params.pop(0) # get rid of first column in results
    sql_params.insert(0, str(uuid.uuid4()))
    sql3_cursor.execute('insert into mm_user_activity (mm_activity_guid, mm_activity_name,'\
        ' mm_activity_overview, mm_activity_short_overview, mm_activity_type,'\
        ' mm_activity_itemid, mm_activity_userid, mm_activity_datecreated,'\
        ' mm_activity_log_severity) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', sql_params)
# close emby db
common_database_emby.com_db_close_emby()
# commit to postgresql
sql3_conn.commit()
# close the db
sql3_conn.close()
