# based on code from
# http://rendykstan.github.io/blog/2013/04/04/postgresql-vacuum-and-analyze-maintenance-and-performance/

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
sys.path.append("../MediaKraken_Server")
sys.path.append("../MediaKraken_Common")
import MK_Commong_Logging
import database as database_base


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_Postgresql_Vacuum')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open_Isolation(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())

# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Postgresql Vacuum Start', None,\
    'System: Server DB Vacuum Start', 'ServerVacuumStart', None, None, 'System')


# vacuum all the tables
# TODO this needed since open is autocommit?   db.MK_Server_Database_Postgesql_Set_Isolation_Level(0)
for row in db.MK_Server_Database_Postgresql_Vacuum_Stat_By_Day(1):
    logging.debug(row)
    db.MK_Server_Database_Postgresql_Vacuum_Table(row['relname'])


# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Postgresql Vacuum Stop', None,\
    'System: Server DB Vacuum Stop', 'ServerVacuumStop', None, None, 'System')


# commit records
db.MK_Server_Database_Commit()


# close the database
db.MK_Server_Database_Close()
