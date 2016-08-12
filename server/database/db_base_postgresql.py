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


# return tables sizes (includex indexes, etc)
# query provided by postgresql wiki
def srv_db_postgresql_table_sizes(self):
    self.sql3_cursor.execute('SELECT nspname || \'.\' || relname AS "relation",'\
        ' pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size" FROM pg_class C'\
        ' LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace) WHERE nspname'\
        ' NOT IN (\'pg_catalog\', \'information_schema\') AND C.relkind <> \'i\''\
        ' AND nspname !~ \'^pg_toast\' ORDER BY pg_total_relation_size(C.oid) DESC')
    return self.sql3_cursor.fetchall()


# return tables and row count
# query provided by postgresql wiki
def srv_db_postgresql_row_count(self):
    self.sql3_cursor.execute('SELECT schemaname,relname,n_live_tup'\
        ' FROM pg_stat_user_tables ORDER BY n_live_tup DESC')
    return self.sql3_cursor.fetchall()


# vacuum stats by day list
def srv_db_postgresql_vacuum_stat_by_day(self, days=1):
    if days == 0:
        self.sql3_cursor.execute('SELECT relname FROM pg_stat_all_tables'\
            ' WHERE schemaname = \'public\'')
    else:
        self.sql3_cursor.execute('SELECT relname FROM pg_stat_all_tables'\
            ' WHERE schemaname = \'public\' AND ((last_analyze is NULL'\
            ' AND last_autoanalyze is NULL) OR ((last_analyze < last_autoanalyze'\
            ' OR last_analyze is null) AND last_autoanalyze < now() - interval %s)'\
            ' OR ((last_autoanalyze < last_analyze OR last_autoanalyze is null)'\
            ' AND last_analyze < now() - interval %s));', [str(days) + ' day', str(days) + ' day'])
    return self.sql3_cursor.fetchall()


# vacuum table
def srv_db_postgresql_vacuum_table(self, table_name):
    self.sql3_cursor.execute('VACUUM ANALYZE ' + table_name)


# set isolation level
def srv_db_postgesql_set_isolation_level(self, isolation_level):
    self.sql3_conn.set_isolation_level(isolation_level)
