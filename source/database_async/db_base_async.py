import os

import asyncpg
from common import common_file
from common import common_global


async def db_table_count(self, table_name):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # All table names will be done by server code, little bobby tables shouldn't apply
    return await self.db_connection.fetchval('select count(*) from ' + table_name)


async def db_open(self, force_local=False, loop=None, as_pool=False):
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
                                                   loop=loop,
                                                   max_size=10)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'db open async'})


async def db_close(self):
    """
    # close main db file
    """
    try:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'db close'})
    except:
        pass
    await self.db_connection.close()


async def db_begin(self):
    """
    # start a transaction
    """
    common_global.es_inst.com_elastic_index('info', {'stuff': 'db begin'})
    await self.db_connection.start()


async def db_commit(self):
    """
    # commit changes to media database
    """
    try:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'db commit'})
    except:
        pass
    await self.db_connection.commit()


async def db_rollback(self):
    """
    # rollback
    """
    common_global.es_inst.com_elastic_index('info', {'stuff': 'db rollback'})
    await self.db_connection.rollback()


async def db_table_index_check(self, resource_name):
    """
    # check for table or index
    """
    # TODO little bobby tables
    self.db_cursor.execute('SELECT to_regclass(\'public.$1\')' % (resource_name,))
    return self.db_cursor.fetchval()


async def db_drop_table(self, table_name):
    """
    drop a table
    """
    # TODO little bobby tables
    await self.db_connection.execute('DROP TABLE IF EXISTS '
                                     + table_name)  # can't %s due to ' inserted


async def db_query(self, query_string, fetch_all=True):
    """
    # general run anything
    """
    # TODO little bobby tables
    try:
        common_global.es_inst.com_elastic_index('info', {"query": query_string})
    except:
        pass
    if fetch_all:
        return await self.db_connection.fetch(query_string)
    else:
        return await self.db_connection.fetchval(query_string)


async def db_parallel_workers(self):
    """
    Return number of workers
    """
    return await self.db_connection.fetchval('show max_parallel_workers_per_gather')
