
def db_pgsql_vacuum_stat_by_day(self, days=1):
    """
    # vacuum stats by day list
    """
    if days == 0:
        self.db_cursor.execute('SELECT relname FROM pg_stat_all_tables'
                               ' WHERE schemaname = \'public\'')
    else:
        self.db_cursor.execute('SELECT relname FROM pg_stat_all_tables'
                               ' WHERE schemaname = \'public\' AND ((last_analyze is NULL'
                               ' AND last_autoanalyze is NULL)'
                               ' OR ((last_analyze < last_autoanalyze'
                               ' OR last_analyze is null)'
                               ' AND last_autoanalyze < now() - interval %s)'
                               ' OR ((last_autoanalyze < last_analyze'
                               ' OR last_autoanalyze is null)'
                               ' AND last_analyze < now() - interval %s));',
                               [str(days) + ' day', str(days) + ' day'])
    return self.db_cursor.fetchall()


def db_pgsql_vacuum_table(self, table_name):
    """
    # vacuum table
    """
    if self.db_pgsql_table_exits(table_name) is not None:
        # self.db_pgsql_set_iso_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.db_cursor.execute('VACUUM ANALYZE ' + table_name)
        # self.db_pgsql_set_iso_level(ISOLATION_LEVEL_READ_COMMITTED)
    else:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'Vacuum table missing': table_name})


def db_pgsql_set_iso_level(self, isolation_level):
    """
    # set isolation level
    """
    self.sql3_conn.set_isolation_level(isolation_level)


def db_pgsql_table_exits(self, table_name):
    """
    Check to see if table exits. Will return NULL if not.
    """
    self.db_cursor.execute('SELECT to_regclass(%s)::text', (table_name,))
    return self.db_cursor.fetchone()[0]

# TODO - see last analynze, etc
# SELECT schemaname, relname, last_analyze FROM pg_stat_all_tables WHERE relname = 'city';
