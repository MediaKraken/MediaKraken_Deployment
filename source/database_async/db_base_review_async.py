import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_review_count(self, metadata_id, db_connection=None):
    """
    # count reviews for media
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
    return await db_conn.fetchval('select count(*) from mm_review'
                                  ' where mm_review_metadata_guid = $1',
                                  metadata_id)


async def db_review_list_by_tmdb_guid(self, metadata_id, db_connection=None):
    """
    # grab reviews for metadata
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
    # TODO order by rating? (optional?)
    return await db_conn.fetch('select mm_review_guid,'
                               'mm_review_json::json'
                               ' from mm_review'
                               ' where mm_review_metadata_id->\'themoviedb\' ? $1',
                               metadata_id)


async def db_review_insert(self, metadata_id, review_json, db_connection=None):
    """
    # insert record
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
    new_guid = str(uuid.uuid4())
    await self.db_cursor.execute('insert into mm_review (mm_review_guid,'
                                 ' mm_review_metadata_id,'
                                 ' mm_review_json::json)'
                                 ' values ($1,$2,$3)',
                                 new_guid, metadata_id, review_json)
    await self.db_cursor.db_commit()
    return new_guid
