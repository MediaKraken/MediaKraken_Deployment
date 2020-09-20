import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_opt_update(self, option_json, db_connection=None):
    """
    Update option json
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
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json = $1',
                          option_json)


async def db_opt_json_read(self, db_connection=None):
    """
    Read options
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
    return await db_conn.fetchval(
        'select mm_options_json::json'
        ' from mm_options_and_status')


async def db_opt_status_read(self, db_connection=None):
    """
    Read options, status
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
    return await db_conn.fetchrow(
        'select mm_options_json::json, mm_status_json::json'
        ' from mm_options_and_status')


async def db_status_json_read(self, db_connection=None):
    """
    Read options
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
    return await db_conn.fetchval(
        'select mm_status_json::json'
        ' from mm_options_and_status')


async def db_opt_status_insert(self, option_json, status_json, db_connection=None):
    """
    insert status
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
    await db_conn.execute('insert into mm_options_and_status'
                          ' (mm_options_and_status_guid,'
                          ' mm_options_json,'
                          ' mm_status_json)'
                          ' values ($1,$2,$3)',
                          uuid.uuid4(), option_json, status_json)
    await db_conn.execute('commit')


async def db_opt_status_update(self, option_json, status_json, db_connection=None):
    """
    Update option and status json
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
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json = $1,'
                          ' mm_status_json = $2',
                          option_json, status_json)
    await db_conn.execute('commit')
