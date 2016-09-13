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


# use this program to update from last alpha
from __future__ import absolute_import, division, print_function, unicode_literals
import subprocess
import os
import sys
sys.path.append("../common")
from common import common_file
import psycopg2


# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn\
    = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()
sql3_cursor2 = sql3_conn.cursor()


if not os.path.exists('update_version.txt'):
    print("Building new table(s)")
    proc_cron = subprocess.Popen(['python', './db_setup/db_setup.py'], shell=False)
    proc_cron.wait()
    common_file.com_file_save_data('update_version.txt', "1")


if common_file.com_file_load_data('update_version.txt', False) == "1":
    print("Building person name index")
    proc_cron = subprocess.Popen(['python', './db_setup/db_setup.py'], shell=False)
    proc_cron.wait()
    common_file.com_file_save_data('update_version.txt', "2")


if common_file.com_file_load_data('update_version.txt', False) == "2":
    print("Adding column for status")
    sql3_cursor.execute("ALTER TABLE mm_media_dir ADD mm_media_dir_status jsonb")
    common_file.com_file_save_data('update_version.txt', "3")


if common_file.com_file_load_data('update_version.txt', False) == "3":
    print("Adding jin index")
    proc_cron = subprocess.Popen(['python', './db_setup/db_setup.py'], shell=False)
    proc_cron.wait()
    common_file.com_file_save_data('update_version.txt', "4")


if common_file.com_file_load_data('update_version.txt', False) == "4":
    print("Adding column name for person")
    sql3_cursor.execute("ALTER TABLE mm_metadata_person ADD mmp_person_name text")
    print("populating person name data")
    sql3_cursor.execute('select mmp_id, mmp_person_meta_json from mm_metadata_person')
    for row_data in sql3_cursor.fetchall():
        sql_params = row_data[1]['Name'], row_data[0]
        sql3_cursor2.execute('update mm_metadata_person set mmp_person_name = %s'\
            ' where mmp_id = %s', sql_params)
    print("creating person name index")
    sql3_cursor.execute('CREATE INDEX mm_metadata_person_idx_name'\
        ' ON mm_metadata_person(mmp_person_name)')
    common_file.com_file_save_data('update_version.txt', "5")


if common_file.com_file_load_data('update_version.txt', False) == "5":
    print("Adding column name for user json to metadata and tvmeta")
    sql3_cursor.execute("ALTER TABLE mm_metadata_movie ADD mm_metadata_user_json jsonb")
    sql3_cursor.execute("ALTER TABLE mm_metadata_tvshow ADD mm_metadata_tvshow_user_json jsonb")
    sql3_conn.commit() # since below is different process must commit first
    print("adding indexs for user json to metadata and tvmeta via db_setup")
    proc_cron = subprocess.Popen(['python', './db_setup/db_setup.py'], shell=False)
    proc_cron.wait()
    common_file.com_file_save_data('update_version.txt', "6")


sql3_conn.commit()
sql3_conn.close()


# git pull the rest
print("Git Pull Common")
os.chdir('../MediaKraken_Common')
proc_cron = subprocess.Popen(['git', 'pull'], shell=False)
proc_cron.wait()


print("Git Pull Server")
os.chdir('../MediaKraken_Server')
proc_cron = subprocess.Popen(['git', 'pull'], shell=False)
proc_cron.wait()

print("Done updating")
