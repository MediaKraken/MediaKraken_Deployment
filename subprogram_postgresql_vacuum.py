# based on code from
# http://rendykstan.github.io/blog/2013/04/04/postgresql-vacuum-and-analyze-maintenance-and-performance/

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from common import common_config_ini
from common import common_logging


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Postgresql_Vacuum')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Postgresql Vacuum Start', None,\
    'System: Server DB Vacuum Start', 'ServerVacuumStart', None, None, 'System')


# vacuum all the tables
for row in db_connection.db_pgsql_vacuum_stat_by_day(1):
    logging.debug(row)
    db_connection.db_pgsql_vacuum_table(row['relname'])


# log end
db_connection.db_activity_insert('MediaKraken_Server Postgresql Vacuum Stop', None,\
    'System: Server DB Vacuum Stop', 'ServerVacuumStop', None, None, 'System')


# commit records
db_connection.db_commit()


# close the database
db_connection.db_close()
