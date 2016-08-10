# based on code from
# http://rendykstan.github.io/blog/2013/04/04/postgresql-vacuum-and-analyze-maintenance-and-performance/

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import logging
import sys
sys.path.append("./")  # for db import
sys.path.append("../MediaKraken_Common")
import MK_Commong_Logging
import database as database_base


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Postgresql_Vacuum')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open_Isolation(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())

# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Postgresql Vacuum Start', None, u'System: Server DB Vacuum Start', u'ServerVacuumStart', None, None, u'System')


# vacuum all the tables
# TODO this needed since open is autocommit?   db.MK_Server_Database_Postgesql_Set_Isolation_Level(0)
for row in db.MK_Server_Database_Postgresql_Vacuum_Stat_By_Day(1):
    logging.debug(row)
    db.MK_Server_Database_Postgresql_Vacuum_Table(row['relname'])


# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Postgresql Vacuum Stop', None, u'System: Server DB Vacuum Stop', u'ServerVacuumStop', None, None, u'System')


# commit records
db.MK_Server_Database_Commit()


# close the database
db.MK_Server_Database_Close()
