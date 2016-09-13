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
import psycopg2


# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn\
    = psycopg2.connect("dbname='metamandb' user='metamanpg' host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()
sql3_cursor2 = sql3_conn.cursor()


def db_table_index_check(resource_name):
    """
    Verify if index exists
    """
    sql3_cursor.execute('SELECT to_regclass(\'public.' + resource_name + '\')')
    query_data = sql3_cursor.fetchone()[0]
    return query_data


print("Dropping mm_link")
sql3_cursor.execute("DROP TABLE IF EXISTS mm_link;")


print("creating table and indexes")
# create table for remote server link
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_link (mm_link_guid uuid'\
    ' CONSTRAINT mm_link_guid_pk PRIMARY KEY, mm_link_name text, mm_link_json jsonb)')
if db_table_index_check('mm_link_json_idxgin') is None:
    sql3_cursor.execute('CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json)')
if db_table_index_check('mm_link_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_link_idx_name ON mm_link(mm_link_name)')


sql3_conn.commit()
sql3_conn.close()


print("Done updating")
