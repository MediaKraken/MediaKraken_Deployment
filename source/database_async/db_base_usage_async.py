import inspect

from common import common_logging_elasticsearch_httpx


async def db_usage_top10_alltime(self, db_connection=None):
    """
    Top 10 of all time
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
    return await db_conn.fetch('select 1 limit 10')


async def db_usage_top10_movie(self, db_connection=None):
    """
    Top 10 movies
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
    return await db_conn.fetch('select mm_metadata_user_json->\'Watched\'->\'Times\''
                               ' from mm_metadata_movie'
                               ' order by mm_metadata_user_json->\'Watched\'->\'Times\''
                               ' desc limit 10')


async def db_usage_top10_tv_episode(self, db_connection=None):
    """
    Top 10 TV episode
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
    return await db_conn.fetch('select 1 limit 10')


async def db_usage_top10_tv_show(self, db_connection=None):
    """
    Top 10 TV show
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
    return await db_conn.fetch('select mm_metadata_tvshow_user_json'
                               '->\'Watched\'->\'Times\''
                               ' from mm_metadata_tvshow'
                               ' order by'
                               ' mm_metadata_tvshow_user_json->\'Watched\'->\'Times\''
                               ' desc limit 10')
