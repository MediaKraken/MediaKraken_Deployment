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
