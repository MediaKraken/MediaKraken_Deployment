import inspect
import json
import os

import asyncpg
from common import common_file
from common import common_logging_elasticsearch_httpx


async def db_table_count(self, table_name, db_connection=None):
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
    return await db_conn.fetchval('select count(*) from ' + table_name)


async def db_open(self, force_local=False, loop=None, as_pool=False):
    """
    # open database
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
    # don't do the db_connection test here.  As this won't be a "separate" pool like webapp
    if force_local:
        database_password = 'metaman'
        database_host = 'localhost'
    else:
        database_host = 'mkstack_database'
        if 'POSTGRES_PASSWORD' in os.environ:
            database_password = os.environ['POSTGRES_PASSWORD']
        else:
            database_password = common_file.com_file_load_data('/run/secrets/db_password')
    if as_pool:
        self.db_connection = await asyncpg.create_pool(user='postgres',
                                                       password='%s' % database_password,
                                                       database='postgres',
                                                       host=database_host,
                                                       loop=loop,
                                                       max_size=50)
    else:
        self.db_connection = await asyncpg.connect(user='postgres',
                                                   password='%s' % database_password,
                                                   database='postgres',
                                                   host=database_host,
                                                   loop=loop)
    await self.db_connection.set_type_codec('jsonb',
                                            encoder=json.dumps,
                                            decoder=json.loads,
                                            schema='pg_catalog')


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


async def db_parallel_workers(self, db_connection=None):
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
