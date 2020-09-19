import inspect

from common import common_logging_elasticsearch_httpx


async def db_meta_music_album_by_guid(self, guid, db_connection=None):
    """
    # return album data by guid
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
    return await db_conn.fetchrow('select * from mm_metadata_album'
                                  ' where mm_metadata_album_guid = $1',
                                  guid)


async def db_meta_music_album_list(self, offset=0, records=None, search_value=None,
                                   db_connection=None):
    """
    # return album metadata list
    """
    # TODO, only grab the poster locale from json
    # TODO order by release year
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
        return await db_conn.fetch('select mm_metadata_album_guid,'
                                   ' mm_metadata_album_name,'
                                   ' mm_metadata_album_json::json,'
                                   ' mm_metadata_album_localimage'
                                   ' from mm_metadata_album'
                                   ' where mm_metadata_album_name % $1'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset $2 limit $3',
                                   search_value,
                                   offset, records)
    else:
        return await db_conn.fetch('select mm_metadata_album_guid,'
                                   ' mm_metadata_album_name,'
                                   ' mm_metadata_album_json::json,'
                                   ' mm_metadata_album_localimage'
                                   ' from mm_metadata_album'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset $1 limit $2',
                                   offset, records)


async def db_meta_music_songs_by_album_guid(self, guid, db_connection=None):
    """
    # return song list from album guid
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
    return await db_conn.fetch('select * from mm_metadata_music'
                               ' where blah = $1'
                               ' order by lower(mm_metadata_music_name)',
                               guid)


async def db_meta_music_song_list(self, offset=0, records=None, search_value=None,
                                  db_connection=None):
    """
    # return song metadata list
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
    # TODO, only grab the poster locale from json
    return {}
