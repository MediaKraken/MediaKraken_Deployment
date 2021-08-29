

async def db_table_count(self, table_name, db_connection=None, exists=False):
    """
    # return count of records in table
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
    # can't %s due to ' inserted
    # All table names will be done by server code, little bobby tables shouldn't apply
    if exists:
        return await db_conn.fetchval('select exists(select 1 from '
                                      + table_name + ' limit 1) limit 1')
    else:
        return await db_conn.fetchval('select count(*) from ' + table_name)


async def db_close(self, db_connection=None):
    """
    # close main db file
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
    await db_conn.close()


async def db_begin(self, db_connection=None):
    """
    # start a transaction
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
    await db_conn.execute('begin')


async def db_commit(self, db_connection=None):
    """
    # commit changes to media database
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
    await db_conn.execute('commit')


async def db_rollback(self, db_connection=None):
    """
    # rollback
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
    await db_conn.execute('rollback')


async def db_table_index_check(self, resource_name, db_connection=None):
    """
    # check for table or index
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
    # TODO little bobby tables
    await self.db_cursor.execute('SELECT to_regclass(\'public.$1\')', resource_name)
    return await self.db_cursor.fetchval()


async def db_drop_table(self, table_name, db_connection=None):
    """
    drop a table
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
    # TODO little bobby tables
    await db_conn.execute('DROP TABLE IF EXISTS '
                          + table_name)  # can't %s due to ' inserted


async def db_query(self, query_string, fetch_all=True, db_connection=None):
    """
    # general run anything
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
    # TODO little bobby tables
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if fetch_all:
        return await db_conn.fetch(query_string)
    else:
        return await db_conn.fetchval(query_string)


def db_parallel_workers(self):
    """
    Return number of workers
    """
    self.db_cursor.execute('show max_parallel_workers_per_gather')
    return self.db_cursor.fetchone()[0]
