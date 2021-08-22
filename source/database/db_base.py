"""
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
"""

import os
import time

import psycopg2
import psycopg2.extras
from common import common_file
from common import common_logging_elasticsearch_httpx
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

def db_close(self):
    """
    # close main db file
    """
    try:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'stuff': 'db close'})
    except:
        pass
    self.sql3_conn.close()


def db_begin(self):
    """
    # start a transaction
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'stuff': 'db begin'})
    self.sql3_conn.begin()


def db_commit(self):
    """
    # commit changes to media database
    """
    try:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'stuff': 'db commit'})
    except:
        pass
    self.sql3_conn.commit()


def db_rollback(self):
    """
    # rollback
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'stuff': 'db rollback'})
    self.sql3_conn.rollback()


def db_table_index_check(self, resource_name):
    """
    # check for table or index
    """
    # TODO little bobby tables
    self.db_cursor.execute('SELECT to_regclass(\'public.%s\')' % (resource_name,))
    return self.db_cursor.fetchone()[0]


def db_table_count(self, table_name, exists=False):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # TODO little bobby tables
    if exists:
        self.db_cursor.execute('select exists(select 1 from ' + table_name + ' limit 1) limit 1 ')
    else:
        self.db_cursor.execute('select count(*) from ' + table_name)
    return self.db_cursor.fetchone()[0]


def db_drop_table(self, table_name):
    """
    drop a table
    """
    # TODO little bobby tables
    self.db_cursor.execute('DROP TABLE IF EXISTS ' + table_name)  # can't %s due to ' inserted


def db_query(self, query_string, fetch_all=True):
    """
    # general run anything
    """
    # TODO little bobby tables
    try:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={"query": query_string})
    except:
        pass
    self.db_cursor.execute(query_string)
    try:
        if fetch_all:
            return self.db_cursor.fetchall()
        else:
            return self.db_cursor.fetchone()[0]
    except:
        return None


def db_parallel_workers(self):
    """
    Return number of workers
    """
    self.db_cursor.execute('show max_parallel_workers_per_gather')
    return self.db_cursor.fetchone()[0]
