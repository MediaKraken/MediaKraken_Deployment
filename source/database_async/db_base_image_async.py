import inspect

from common import common_logging_elasticsearch_httpx


async def db_image_count(self, class_guid, search_value=None, db_connection=None):
    """
    Image list count
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
    return await db_conn.fetchval('select count(*) from mm_media'
                                  ' where mm_media_class_guid = $1', class_guid)


async def db_image_list(self, class_guid, offset=0, records=None, search_value=None,
                        db_connection=None):
    """
    Image list
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
    return await db_conn.fetch('select mm_media_path from mm_media'
                               ' where mm_media_class_guid = $1 offset $2 limit $3',
                               class_guid, offset, records)
