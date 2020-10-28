import inspect
import uuid
from common import common_logging_elasticsearch_httpx


async def db_meta_game_by_guid(self, guid, db_connection=None):
    """
    # return game data
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
    return await db_conn.fetchrow('select gi_id,'
                                  ' gi_system_id,'
                                  ' gi_game_info_json'
                                  ' from mm_metadata_game_software_info'
                                  ' where gi_id = $1', guid)


async def db_meta_game_by_sha1(self, sha1_hash, db_connection=None):
    """
    # return game uuid by sha1 hash
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
    return await db_conn.fetchval('select gi_id'
                                  ' from mm_metadata_game_software_info'
                                  ' where gi_game_info_sha1 = $1',
                                  sha1_hash)


async def db_meta_game_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    # return list of games
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
        return await db_conn.fetch('select gi_id,gi_game_info_short_name,'
                                   ' gi_game_info_name,'
                                   ' gi_game_info_json->\'year\','
                                   ' gs_game_system_json->\'description\''
                                   ' from mm_metadata_game_software_info,'
                                   ' mm_metadata_game_systems_info'
                                   ' where gi_system_id = gs_id'
                                   ' and gi_game_info_name % $1'
                                   ' order by gi_game_info_name,'
                                   ' gi_game_info_json->\'year\''
                                   ' offset $2 limit $3',
                                   search_value,
                                   offset, records)
    else:
        return await db_conn.fetch('select gi_id,gi_game_info_short_name,'
                                   ' gi_game_info_name,'
                                   ' gi_game_info_json->\'year\','
                                   ' gs_game_system_json->\'description\''
                                   ' from mm_metadata_game_software_info,'
                                   ' mm_metadata_game_systems_info'
                                   ' where gi_system_id = gs_id'
                                   ' order by gi_game_info_name,'
                                   ' gi_game_info_json->\'year\''
                                   ' offset $1 limit $2',
                                   offset, records)


async def db_meta_game_insert(self, game_system_id, game_short_name, game_name, game_json,
                              db_connection=None):
    """
    Insert game
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
    new_game_id = uuid.uuid4()
    await db_conn.execute('insert into mm_metadata_game_software_info(gi_id, gi_system_id,'
                          ' gi_game_info_short_name,'
                          ' gi_game_info_name,'
                          ' gi_game_info_json)'
                          ' values ($1, $2, $3, $4, $5)',
                          new_game_id, game_system_id, game_short_name, game_name,
                          game_json)
    return new_game_id


async def db_meta_game_update(self, game_system_id, game_short_name, game_name, game_json,
                              db_connection=None):
    """
    Update game
   async """
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
    await db_conn.execute('update mm_metadata_game_software_info set gi_game_info_json = $1'
                          ' where gi_system_id = $2 and gi_game_info_short_name = $3'
                          ' and gi_game_info_name = $4',
                          game_json, game_system_id, game_short_name, game_name)


async def db_meta_game_by_name(self, game_short_name, game_name, db_connection=None):
    """
    # return game info by name
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
    return await db_conn.fetch('select gi_id, gi_system_id,'
                               ' gi_game_info_json'
                               ' from mm_metadata_game_software_info'
                               ' where gi_game_info_name = $1'
                               ' or game_short_name = $2', game_name, game_short_name)


async def db_meta_game_update_by_guid(self, game_id, game_json, db_connection=None):
    """
    Update game by uuid
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
    await db_conn.execute('update mm_metadata_game_software_info set gi_game_info_json = $1'
                          ' where gi_system_id = $2',
                          game_json, game_id)
