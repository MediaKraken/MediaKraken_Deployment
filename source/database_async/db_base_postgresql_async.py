
async def db_pgsql_vacuum_stat_by_day(self, days=1, db_connection=None):
    """
    # vacuum stats by day list
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if days == 0:
        return await db_conn.fetch('SELECT relname FROM pg_stat_all_tables'
                               ' WHERE schemaname = \'public\'')
    else:
        return await db_conn.fetch('SELECT relname FROM pg_stat_all_tables'
                               ' WHERE schemaname = \'public\' AND ((last_analyze is NULL'
                               ' AND last_autoanalyze is NULL)'
                               ' OR ((last_analyze < last_autoanalyze'
                               ' OR last_analyze is null)'
                               ' AND last_autoanalyze < now() - interval $1)'
                               ' OR ((last_autoanalyze < last_analyze'
                               ' OR last_autoanalyze is null)'
                               ' AND last_analyze < now() - interval $2));',
                               str(days) + ' day', str(days) + ' day')
