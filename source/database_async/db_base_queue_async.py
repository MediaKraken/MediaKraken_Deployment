import inspect

from common import common_logging_elasticsearch_httpx


async def db_meta_queue_list_count(self, user_id, search_value=None, db_connection=None):
    """
    Return count of queued media for user
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
    if search_value is not None:
        return await db_conn.fetchval('select count(*)'
                                      ' from mm_user_queue'
                                      ' where mm_user_queue_name % $1'
                                      ' and mm_user_queue_user_id = $2',
                                      search_value, user_id)
    else:
        return await db_conn.fetchval('select count(*) from mm_user_queue'
                                      ' where mm_user_queue_user_id = $1', user_id)
