import inspect

from common import common_logging_elasticsearch_httpx


async def db_media_mame_game_list(self, db_connection=None):
    """
    Game systems are NULL for MAME
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
    await db_conn.fetch('select gi_id, gi_short_name'
                        ' from mm_game_info'
                        ' where gi_system_id is null'
                        ' and gi_gc_category is null')


async def db_media_game_category_update(self, category, game_id, db_connection=None):
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
    await db_conn.execute('update mm_game_info'
                          ' set gi_gc_category = $1'
                          ' where gi_id = $2', category, game_id)
    await db_conn.execute('commit')


async def db_media_game_clone_list(self, db_connection=None):
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
    return await db_conn.fetch('select gi_id,'
                               ' gi_cloneof'
                               ' from mm_game_info'
                               ' where gi_system_id is null'
                               ' and gi_cloneof IS NOT NULL'
                               ' and gi_gc_category is null')


async def db_media_game_category_by_name(self, category_name, db_connection=None):
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
    await db_conn.fetchval('select gi_gc_category'
                           ' from mm_game_info'
                           ' where gi_short_name = $1', category_name)
