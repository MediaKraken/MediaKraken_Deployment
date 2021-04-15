import inspect
import json
import uuid

from common import common_logging_elasticsearch_httpx


async def db_game_server_list(self, offset=0, records=None, db_connection=None):
    """
    Return game server list
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
    return await db_conn.fetch('select mm_game_server_guid,'
                               ' mm_game_server_name,'
                               ' mm_game_server_json'
                               ' from mm_game_dedicated_servers'
                               ' order by mm_game_server_name offset $1 limit $2',
                               offset, records)


async def db_game_server_upsert(self, server_name, server_json, db_connection=None):
    """
    Upsert a game server into the database
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
    new_guid = uuid.uuid4()
    await db_conn.execute('INSERT INTO mm_game_dedicated_servers (mm_game_server_guid,'
                          ' mm_game_server_name,'
                          ' mm_game_server_json)'
                          ' VALUES ($1, $2, $3)'
                          ' ON CONFLICT (mm_game_server_name)'
                          ' DO UPDATE SET mm_game_server_json = $4',
                          new_guid, server_name, json.dumps(server_json),
                          json.dumps(server_json))
    return new_guid


async def db_game_server_insert(self, game_server_name, game_server_json, db_connection=None):
    """
    insert game server
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
    new_id = uuid.uuid4()
    await db_conn.execute('insert into mm_game_dedicated_servers (mm_game_server_guid,'
                          ' mm_game_server_name,'
                          ' mm_game_server_json)'
                          ' values ($1,$2,$3)',
                          new_id, game_server_name, game_server_json)
    return new_id


async def db_game_server_delete(self, record_uuid, db_connection=None):
    """
    Delete game_server
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
    await db_conn.execute('delete from mm_game_dedicated_servers'
                          ' where mm_game_server_guid = $1',
                          record_uuid)


async def db_game_server_detail(self, record_uuid, db_connection=None):
    """
    game server info
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
    return await db_conn.fetchrow('select mm_game_server_name,'
                                  ' mm_game_server_json'
                                  ' from mm_game_dedicated_servers'
                                  ' where mm_game_server_guid = %s', record_uuid)


async def db_game_server_list_count(self, db_connection=None):
    """
    Return number of game servers
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
    return await db_conn.fetchval('select count(*) from mm_game_dedicated_servers')
