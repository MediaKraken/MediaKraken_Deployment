import inspect

from common import common_logging_elasticsearch_httpx


async def db_link_delete(self, sync_guid, db_connection=None):
    """
    Delete server link
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
    await db_conn.execute('delete from mm_link where mm_link_guid = $1', sync_guid)


async def db_link_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    Return list of linked server
    Complete list for admins
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
        return await db_conn.fetch('select mm_link_guid,'
                                   ' mm_link_name,'
                                   ' mm_link_json::json'
                                   ' from mm_link'
                                   ' where mm_link_guid in (select mm_link_guid'
                                   ' from mm_link'
                                   ' where mm_link_name % $1 offset $2 limit $3)',
                                   search_value, offset, records)
    else:
        return await db_conn.fetch('select mm_link_guid,'
                                   ' mm_link_name,'
                                   ' mm_link_json::json'
                                   ' from mm_link'
                                   ' where mm_link_guid in (select mm_link_guid'
                                   ' from mm_link'
                                   ' offset $1 limit $2)',
                                   offset, records)


async def db_link_list_count(self, search_value=None, db_connection=None):
    """
    Return count of linked servers
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
                                      ' from mm_link where mm_link_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*) from mm_link')
