import inspect

from common import common_logging_elasticsearch_httpx


async def db_music_video_list(self, offset=0, per_page=None, search_value=None, db_connection=None):
    """
    music video list
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
    pass


async def db_music_video_list_count(self, search_value=None, db_connection=None):
    """
    Music video count
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
                                      ' from mm_metadata_music_video, mm_media'
                                      ' where mm_media_metadata_guid'
                                      ' = mm_metadata_music_video_guid group'
                                      ' and mm_media_music_video_song % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*)'
                                      ' from mm_metadata_music_video, mm_media'
                                      ' where mm_media_metadata_guid'
                                      ' = mm_metadata_music_video_guid')
