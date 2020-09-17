import json
import os

import asyncpg
from common import common_file
from common import common_logging_elasticsearch_httpx


async def db_table_count(self, table_name, db_connection=None):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # All table names will be done by server code, little bobby tables shouldn't apply
    return await self.db_connection.fetchval('select count(*) from ' + table_name)


async def db_open(self, force_local=False, loop=None, as_pool=False, db_connection=None):
    """
    # open database
    """
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
    await self.db_connection.set_type_codec('json',
                                            encoder=json.dumps,
                                            decoder=json.loads,
                                            schema='pg_catalog')
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'stuff': 'db open async'})


async def db_close(self, db_connection=None):
    """
    # close main db file
    """
    try:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'db close'})
    except:
        pass
    await self.db_connection.close()


async def db_begin(self, db_connection=None):
    """
    # start a transaction
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'stuff': 'db begin'})
    await self.db_connection.start()


async def db_commit(self, db_connection=None):
    """
    # commit changes to media database
    """
    try:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'db commit'})
    except:
        pass
    await self.db_connection.commit()


async def db_rollback(self, db_connection=None):
    """
    # rollback
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'stuff': 'db rollback'})
    await self.db_connection.rollback()


async def db_table_index_check(self, resource_name, db_connection=None):
    """
    # check for table or index
    """
    # TODO little bobby tables
    self.db_cursor.execute('SELECT to_regclass(\'public.$1\')', resource_name)
    return self.db_cursor.fetchval()


async def db_drop_table(self, table_name, db_connection=None):
    """
    drop a table
    """
    # TODO little bobby tables
    await self.db_connection.execute('DROP TABLE IF EXISTS '
                                     + table_name)  # can't %s due to ' inserted


async def db_query(self, query_string, fetch_all=True, db_connection=None):
    """
    # general run anything
    """
    # TODO little bobby tables
    try:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "query": query_string})
    except:
        pass
    if fetch_all:
        return await self.db_connection.fetch(query_string)
    else:
        return await self.db_connection.fetchval(query_string)


async def db_parallel_workers(self, db_connection=None):
    """
    Return number of workers
    """
    return await self.db_connection.fetchval('show max_parallel_workers_per_gather')
