import inspect

from common import common_logging_elasticsearch_httpx


async def db_media_album_count(self, search_value=None, db_connection=None):
    """
    Album count
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
        return await db_conn.fetchval('select count(*) from mm_metadata_album, mm_media'
                                      ' where mm_media_metadata_guid'
                                      ' = mm_metadata_album_guid '
                                      ' and mm_metadata_album_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval(
            'select count(*) from (select distinct mm_metadata_album_guid'
            ' from mm_metadata_album, mm_media'
            ' where mm_media_metadata_guid = mm_metadata_album_guid) as temp')


async def db_media_album_list(self, offset=0, per_page=None, search_value=None, db_connection=None):
    """
    Album list
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
    # TODO only grab the image part of the json for list, might want runtime, etc as well
    if search_value is not None:
        return await db_conn.fetch('select mm_metadata_album_guid,'
                                   ' mm_metadata_album_name,'
                                   ' mm_metadata_album_json::json'
                                   ' from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid'
                                   ' = mm_metadata_album_guid'
                                   ' and mm_metadata_album_name % $1'
                                   ' group by mm_metadata_album_guid'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset $2 limit $3',
                                   search_value, offset, per_page)
    else:
        return await db_conn.fetch('select mm_metadata_album_guid,'
                                   ' mm_metadata_album_name,'
                                   ' mm_metadata_album_json::json'
                                   ' from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid'
                                   ' = mm_metadata_album_guid'
                                   ' group by mm_metadata_album_guid'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset $1 limit $2',
                                   offset, per_page)
