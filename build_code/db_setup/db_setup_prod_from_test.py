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
import subprocess
import time

# functions to deal with database data
sql3_conn = None
sql3_cursor = None

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn\
     = psycopg2.connect("dbname='metamandb' user='metamanpg'"\
     " host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()
sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class WHERE relname = 'mm_media'")
if sql3_cursor.fetchone()[0] == 0:
    # truncate data
    sql3_cursor.execute('truncate '\
        'mm_channel,'\
        'mm_device,'\
        'mm_download_que,'\
        'mm_link,'\
        'mm_loan,'\
        'mm_media,'\
        'mm_media_dir,'\
        'mm_media_remote,'\
        'mm_notification,'\
        'mm_nas,'\
        'mm_sync,'\
        'mm_trigger,'\
        'mm_tv_schedule,'\
        'mm_tv_schedule_program,'\
        'mm_tv_stations,'\
        'mm_user,'\
        'mm_user_activity,'\
        'mm_tuner')
    sql3_conn.commit()
    # create dump file
    proc = subprocess.Popen(['pg_dump', '-Fc', 'metamandb', '>',\
        './MediaKraken_SQL_Dump' + '_' + time.strftime("%Y%m%d%H%M%S") + '.dump'],\
        shell=False)
    print("PG dump PID: %s", proc.pid)
    proc.wait()
# close the DB
sql3_conn.close()
