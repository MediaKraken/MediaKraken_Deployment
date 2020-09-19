import inspect

from common import common_logging_elasticsearch_httpx


async def db_pgsql_parallel_workers(self, db_connection=None):
    """
    Return number of workers
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
    return await db_conn.fetchval('show max_parallel_workers_per_gather')


# query provided by postgresql wiki
async def db_pgsql_row_count(self, db_connection=None):
    """
    # return tables and row count
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
    return await db_conn.fetch(
        'SELECT nspname AS schemaname,relname,reltuples FROM pg_class C'
        ' LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)'
        ' WHERE nspname NOT IN (\'pg_catalog\', \'information_schema\')'
        ' AND relkind=\'r\' ORDER BY reltuples DESC')


# query provided by postgresql wiki
async def db_pgsql_table_sizes(self, db_connection=None):
    """
    # return tables sizes (includes indexes, etc)
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
    return await db_conn.fetch('SELECT nspname || \'.\' || relname AS "relation",'
                               ' pg_total_relation_size(C.oid) AS "total_size"'
                               ' FROM pg_class C'
                               ' LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)'
                               ' WHERE nspname'
                               ' NOT IN (\'pg_catalog\', \'information_schema\')'
                               ' AND C.relkind <> \'i\''
                               ' AND nspname !~ \'^pg_toast\''
                               ' ORDER BY pg_total_relation_size(C.oid) DESC')
