"""
Vacuum tables
"""
# based on code from
# http://rendykstan.github.io/blog/2013/04/04/postgresql-vacuum-and-analyze-maintenance-and-performance/

import sys

from common import common_config_ini
from common import common_logging_elasticsearch_httpx
from common import common_signal
from common import common_system

# verify this program isn't already running!
if common_system.com_process_list(
        process_name='/usr/bin/python3 /mediakraken/subprogram_postgresql_vacuum.py'):
    sys.exit(0)

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='subprogram_postgresql_vacuum')
# set signal exit breaks
common_signal.com_signal_set_break()
# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# vacuum all the tables
for row in db_connection.db_pgsql_vacuum_stat_by_day(1):
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'row': row})
    db_connection.db_pgsql_vacuum_table(row['relname'])

# commit records
db_connection.db_commit()

# close the database
db_connection.db_close()
