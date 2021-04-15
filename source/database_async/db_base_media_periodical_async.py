import inspect

from common import common_logging_elasticsearch_httpx


async def db_media_book_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    book list
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
        return await db_conn.fetch('select mm_metadata_book_guid,'
                                   ' mm_metadata_book_name'
                                   ' from mm_metadata_book, mm_media'
                                   ' where mm_media_metadata_guid'
                                   ' = mm_metadata_book_guid '
                                   ' and mm_metadata_book_name % $1'
                                   ' order by LOWER(mm_metadata_book_name)'
                                   ' offset $2 limit $3',
                                   search_value, offset, records)
    else:
        return await db_conn.fetch('select mm_metadata_book_guid,'
                                   ' mm_metadata_book_name'
                                   ' from mm_metadata_book, mm_media'
                                   ' where mm_media_metadata_guid'
                                   ' = mm_metadata_book_guid'
                                   ' order by LOWER(mm_metadata_book_name)'
                                   ' offset $1 limit $2',
                                   offset, records)


async def db_media_book_list_count(self, search_value=None, db_connection=None):
    """
    book list count
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
        return await db_conn.fetchval('select count(*) from mm_metadata_book,'
                                      ' mm_media'
                                      ' where mm_media_metadata_guid'
                                      ' = mm_metadata_book_guid '
                                      'and mm_metadata_book_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*) from mm_metadata_book,'
                                      ' mm_media'
                                      ' where mm_media_metadata_guid'
                                      ' = mm_metadata_book_guid')
