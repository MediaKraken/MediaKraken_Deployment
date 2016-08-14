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
import logging
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED # the default
from psycopg2.extras import DictCursor
from db_base_postgresql_ext import *


def srv_db_open(self, PostDBHost, PostDBPort, PostDBName, PostDBUser, PostDBPass):
    """
    # open database and pull in config from sqlite and create db if not exist
    """
    # setup for unicode
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    #psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
    #psycopg2.extras.register_default_json(loads=lambda x: x)
    self.sql3_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'"\
        % (PostDBName, PostDBUser, PostDBHost, int(PostDBPort), PostDBPass))
    self.sql3_cursor = self.sql3_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    self.sql3_cursor.execute("SET TIMEZONE = 'America/Chicago'")
    self.sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class'\
        ' WHERE relname = 'mm_media'")
    if self.sql3_cursor.fetchone()['a'] == 0:
        logging.critical("Database is not populated!")
        sys.exit()


def srv_db_open_isolation(self, PostDBHost, PostDBPort, PostDBName,\
        PostDBUser, PostDBPass):
    """
    # open database and pull in config from sqlite and create db if not exist
    """
    # setup for unicode
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    #psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
    #psycopg2.extras.register_default_json(loads=lambda x: x)
    self.sql3_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'"\
        % (PostDBName, PostDBUser, PostDBHost, int(PostDBPort), PostDBPass))
    self.sql3_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    self.sql3_cursor = self.sql3_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    self.sql3_cursor.execute("SET TIMEZONE = 'America/Chicago'")
    self.sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class'\
        ' WHERE relname = 'mm_media'")
    if self.sql3_cursor.fetchone()['a'] == 0:
        logging.critical("Database is not populated!")
        sys.exit()


def srv_db_close(self):
    """
    # close main db file
    """
    self.sql3_conn.close()


def srv_db_commit(self):
    """
    # commit changes to media database
    """
    self.sql3_conn.commit()


def srv_db_rollback(self):
    """
    # rollback
    """
    self.sql3_conn.rollback()


def srv_db_table_index_check(self, resource_name):
    """
    # check for table or index
    """
    self.sql3_cursor.execute('SELECT to_regclass(\'public.%s\')', (resource_name,))
    return self.sql3_cursor.fetchone()[0]


def srv_db_table_count(self, table_name):
    """
    # return count of records in table
    """
    self.sql3_cursor.execute('select count(*) from ' + table_name) # can't %s due to ' inserted
    return self.sql3_cursor.fetchone()[0]


def srv_db_query(self, query_string):
    """
    # general run anything
    """
    logging.debug("query: %s", query_string)
    self.sql3_cursor.execute(query_string)
    return self.sql3_cursor.fetchall()
