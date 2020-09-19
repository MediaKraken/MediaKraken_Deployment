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
                               ' mm_game_server_json::json'
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
    new_guid = str(uuid.uuid4())
    await db_conn.execute('INSERT INTO mm_game_dedicated_servers (mm_game_server_guid,'
                          ' mm_game_server_name,'
                          ' mm_game_server_json::json)'
                          ' VALUES ($1, $2, $3)'
                          ' ON CONFLICT (mm_game_server_name)'
                          ' DO UPDATE SET mm_game_server_json = $4',
                          new_guid, server_name, json.dumps(server_json),
                          json.dumps(server_json))
    return new_guid
