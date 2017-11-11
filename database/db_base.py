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
import logging # pylint: disable=W0611
import os
from common import common_system
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # pylint: disable=W0611
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED # the default
from psycopg2.extras import DictCursor # pylint: disable=W0611


def db_open(self, db_build=False):
    """
    # open database and pull in config and create db if not exist
    """
    # setup for unicode
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    #psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
    #psycopg2.extras.register_default_json(loads=lambda x: x)
    if db_build == True:
        self.sql3_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'"\
            % (os.environ['POSTGRES_DB'], os.environ['POSTGRES_USER'], 'mkpgbounce', 6432,
            os.environ['POSTGRES_PASSWORD']))
    else:
        self.sql3_conn = psycopg2.connect("dbname='metamandb' user='metamanpg'"
                                          " host='10.0.0.42' port=5432 password='metamanpg'")
    self.sql3_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    #self.sql3_conn.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    self.db_cursor = self.sql3_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    self.db_cursor.execute('SET TIMEZONE = \'America/Chicago\'')
    self.db_cursor.execute('SET max_parallel_workers_per_gather TO %s;' %
                           common_system.com_system_cpu_count())


def db_close(self):
    """
    # close main db file
    """
    logging.info('db close')
    self.sql3_conn.close()


def db_commit(self):
    """
    # commit changes to media database
    """
    logging.info('db commit')
    self.sql3_conn.commit()


def db_rollback(self):
    """
    # rollback
    """
    logging.info('db rollback')
    self.sql3_conn.rollback()


def db_table_index_check(self, resource_name):
    """
    # check for table or index
    """
    self.db_cursor.execute('SELECT to_regclass(\'public.%s\')' % (resource_name,))
    return self.db_cursor.fetchone()[0]


def db_table_count(self, table_name):
    """
    # return count of records in table
    """
    try:
        self.db_cursor.execute('select count(*) from ' + table_name) # can't %s due to ' inserted
        return self.db_cursor.fetchone()[0]
    except:
        return None


def db_drop_table(self, table_name):
    """
    drop a table
    """
    self.db_cursor.execute('DROP TABLE IF EXISTS ' + table_name) # can't %s due to ' inserted


def db_query(self, query_string):
    """
    # general run anything
    """
    logging.info("query: %s", query_string)
    self.db_cursor.execute(query_string)
    try:
        return self.db_cursor.fetchall()
    except:
        return None


def db_parallel_workers(self):
    """
    Return number of workers
    """
    self.db_cursor.execute('show max_parallel_workers_per_gather')
    return self.db_cursor.fetchone()[0]
