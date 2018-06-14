"""
Vacuum tables
"""
# based on code from
# http://rendykstan.github.io/blog/2013/04/04/postgresql-vacuum-and-analyze-maintenance-and-performance/


from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_postgresql_vacuum')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# vacuum all the tables
for row in db_connection.db_pgsql_vacuum_stat_by_day(1):
    common_global.es_inst.com_elastic_index('info', {'row': row})
    db_connection.db_pgsql_vacuum_table(row['relname'])

# commit records
db_connection.db_commit()

# close the database
db_connection.db_close()
