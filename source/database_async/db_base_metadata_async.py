import inspect

from common import common_logging_elasticsearch_httpx


async def db_metadata_guid_from_media_guid(self, guid, db_connection=None):
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
    return await db_conn.fetchval('select mm_media_metadata_guid'
                                  ' from mm_media'
                                  ' where mm_media_guid = $1', guid)


async def db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json,
                              data_image_json, db_connection=None):
    """
    # insert metadata from themoviedb
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
    await db_conn.execute('insert into mm_metadata_movie (mm_metadata_guid,'
                          ' mm_metadata_media_id,'
                          ' mm_metadata_name,'
                          ' mm_metadata_json,'
                          ' mm_metadata_localimage_json)'
                          ' values ($1,$2,$3,$4,$5)',
                          uuid_id, series_id, data_title,
                          data_json, data_image_json)
    await db_conn.execute('commit')


async def db_meta_guid_by_imdb(self, imdb_uuid, db_connection=None):
    """
    # metadata guid by imdb id
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
    return await db_conn.fetchval('select mm_metadata_guid'
                                  ' from mm_metadata_movie'
                                  ' where mm_metadata_media_id->\'imdb\' ? $1',
                                  imdb_uuid)


async def db_meta_guid_by_tmdb(self, tmdb_uuid, db_connection=None):
    """
    # see if metadata exists type and id
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
    return await db_conn.fetchval('select mm_metadata_guid'
                                  ' from mm_metadata_movie'
                                  ' where mm_metadata_media_id = $1',
                                  tmdb_uuid)


async def db_find_metadata_guid(self, media_name, media_release_year, db_connection=None):
    """
    Lookup id by name/year
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
    metadata_guid = None
    if media_release_year is not None:
        # for year and -3/+3 year as well
        meta_results = await db_conn.fetch('select mm_metadata_guid from mm_metadata_movie'
                                           ' where (LOWER(mm_metadata_name) = $1'
                                           ' or lower(mm_metadata_json->>\'original_title\') = $2)'
                                           ' and substring(mm_metadata_json->>\'release_date\''
                                           ' from 0 for 5)'
                                           ' in ($3,$4,$5,$6,$7,$8,$9)',
                                           media_name.lower(), media_name.lower(),
                                           str(media_release_year),
                                           str(int(media_release_year) + 1),
                                           str(int(media_release_year) + 2),
                                           str(int(media_release_year) + 3),
                                           str(int(media_release_year) - 1),
                                           str(int(media_release_year) - 2),
                                           str(int(media_release_year) - 3))
    else:
        meta_results = await db_conn.fetch('select mm_metadata_guid from mm_metadata_movie'
                                           ' where (LOWER(mm_metadata_name) = $1'
                                           ' or lower(mm_metadata_json->>\'original_title\') = $2)',
                                           media_name.lower(), media_name.lower())
    for row_data in meta_results:
        # TODO should probably handle multiple results better.   Perhaps a notification?
        metadata_guid = row_data['mm_metadata_guid']
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "db find metadata guid": metadata_guid})
        break
    return metadata_guid
