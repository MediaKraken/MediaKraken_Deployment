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
from common import common_global
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED


def db_open(self, force_local=False):
    """
    # open database
    """
    # setup for unicode
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    # psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
    # psycopg2.extras.register_default_json(loads=lambda x: x)
    if force_local:
        self.sql3_conn = psycopg2.connect(
            "dbname='postgres' user='postgres' host='localhost'"
            " port=5432 password='metaman' connect_timeout=5")
    else:
        # this is here to handle going back to docker-compose with else for docker swarm
        if 'POSTGRES_PASSWORD' in os.environ:
            database_password = os.environ['POSTGRES_PASSWORD']
        else:
            database_password = common_file.com_file_load_data('/run/secrets/db_password')
        # keep trying to connect every 10 seconds, hence sleep later in while
        while True:
            try:
                self.sql3_conn = psycopg2.connect(
                    "dbname='postgres' user='postgres' host='mkstack_pgbouncer'"
                    " port=6432 password='%s' connect_timeout=5"  # , async=1 - invalid option
                    % database_password.strip())
            except (psycopg2.OperationalError, psycopg2.DatabaseError):
                time.sleep(10)
            else:
                break
        common_global.es_inst.com_elastic_index('info', {'stuff': 'db open'})
    self.db_cursor = self.sql3_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def db_close(self):
    """
    # close main db file
    """
    try:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'db close'})
    except:
        pass
    self.sql3_conn.close()


def db_begin(self):
    """
    # start a transaction
    """
    common_global.es_inst.com_elastic_index('info', {'stuff': 'db begin'})
    self.sql3_conn.begin()


def db_commit(self):
    """
    # commit changes to media database
    """
    try:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'db commit'})
    except:
        pass
    self.sql3_conn.commit()


def db_rollback(self):
    """
    # rollback
    """
    common_global.es_inst.com_elastic_index('info', {'stuff': 'db rollback'})
    self.sql3_conn.rollback()


def db_table_index_check(self, resource_name):
    """
    # check for table or index
    """
    # TODO little bobby tables
    self.db_cursor.execute('SELECT to_regclass(\'public.%s\')' % (resource_name,))
    return self.db_cursor.fetchone()[0]


def db_table_count(self, table_name):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # TODO little bobby tables
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
        common_global.es_inst.com_elastic_index('info', {"query": query_string})
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
