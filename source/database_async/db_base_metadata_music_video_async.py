import inspect

from common import common_logging_elasticsearch_httpx


async def db_meta_music_video_lookup(self, artist_name, song_title, db_connection=None):
    """
    # query to see if song is in local DB
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
    return await db_conn.fetch('select mm_metadata_music_video_guid from mm_metadata_music_video'
                               ' where lower(mm_media_music_video_band) = $1'
                               ' and lower(mm_media_music_video_song) = $2',
                               artist_name.lower(), song_title.lower())


async def db_meta_music_video_add(self, new_guid, artist_name, artist_song, id_json,
                                  data_json, image_json, db_connection=None):
    """
    Add metadata for music video
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
    await db_conn.execute('insert into mm_metadata_music_video (mm_metadata_music_video_guid,'
                          ' mm_metadata_music_video_media_id,'
                          ' mm_media_music_video_band,'
                          ' mm_media_music_video_song,'
                          ' mm_metadata_music_video_json,'
                          ' mm_metadata_music_video_localimage_json)'
                          ' values ($1,$2,$3,$4,$5,$6)',
                          new_guid, id_json, artist_name, artist_song, data_json, image_json)
    await db_conn.db_commit()
    return new_guid


async def db_meta_music_video_count(self, imvdb_id=None, search_value=None, db_connection=None):
    """
    Return count of music video metadata
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
    if imvdb_id is None:
        if search_value is not None:
            return await db_conn.fetchval('select count(*) from mm_metadata_music_video'
                                          ' where mm_media_music_video_song % $1',
                                          search_value)
        else:
            return await db_conn.fetchval(
                'select count(*) from mm_metadata_music_video')
    else:
        return await db_conn.fetchval('select count(*) from mm_metadata_music_video'
                                      ' where mm_metadata_music_video_media_id->\'imvdb\' ? $1',
                                      imvdb_id)


async def db_meta_music_video_detail_uuid(self, item_guid, db_connection=None):
    """
    Grab metadata for specified music video
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
    return await db_conn.fetchrow('select mm_media_music_video_band,'
                                  ' mm_media_music_video_song,'
                                  ' mm_metadata_music_video_json,'
                                  ' mm_metadata_music_video_localimage_json'
                                  ' from mm_metadata_music_video'
                                  ' where mm_metadata_music_video_guid = $1',
                                  item_guid)


async def db_meta_music_video_list(self, offset=0, records=None, search_value=None,
                                   db_connection=None):
    """
    List music video metadata
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
    # TODO order by release date
    if search_value is not None:
        return await db_conn.fetch('select mm_metadata_music_video_guid,'
                                   ' mm_media_music_video_band,'
                                   ' mm_media_music_video_song,'
                                   ' mm_metadata_music_video_localimage_json'
                                   ' from mm_metadata_music_video'
                                   ' where mm_media_music_video_song % $1'
                                   ' order by LOWER(mm_media_music_video_band),'
                                   ' LOWER(mm_media_music_video_song)'
                                   ' offset $2 limit $3',
                                   search_value, offset, records)
    else:
        return await db_conn.fetch('select mm_metadata_music_video_guid,'
                                   ' mm_media_music_video_band,'
                                   ' mm_media_music_video_song,'
                                   ' mm_metadata_music_video_localimage_json'
                                   ' from mm_metadata_music_video'
                                   ' order by LOWER(mm_media_music_video_band),'
                                   ' LOWER(mm_media_music_video_song)'
                                   ' offset $1 limit $2',
                                   offset, records)
