import inspect

from common import common_logging_elasticsearch_httpx


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
                               ' mm_review_json::json'
                               ' from mm_review'
                               ' where mm_review_metadata_id = $1',
                               str(metadata_id))
