import inspect

from common import common_logging_elasticsearch_httpx


async def db_3d_list_count(self, search_value=None):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    return 0


async def db_3d_list(self, offset=None, records=None, search_value=None, db_connection=None):
    """
    Return collections list from the database
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return None
