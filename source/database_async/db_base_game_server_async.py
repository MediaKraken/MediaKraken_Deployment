import json
import uuid


async def db_game_server_list(self, offset=0, records=None):
    """
    Return game server list
    """
    return await self.db_connection.fetch('select mm_game_server_guid,'
                                          ' mm_game_server_name,'
                                          ' mm_game_server_json::json'
                                          ' from mm_game_dedicated_servers'
                                          ' order by mm_game_server_name offset $1 limit $2',
                                          offset, records)


async def db_game_server_upsert(self, server_name, server_json):
    """
    Upsert a game server into the database
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('INSERT INTO mm_game_dedicated_servers (mm_game_server_guid,'
                                     ' mm_game_server_name,'
                                     ' mm_game_server_json::json)'
                                     ' VALUES ($1, $2, $3)'
                                     ' ON CONFLICT (mm_game_server_name)'
                                     ' DO UPDATE SET mm_game_server_json = $4',
                                     new_guid, server_name, json.dumps(server_json),
                                     json.dumps(server_json))
    return new_guid
