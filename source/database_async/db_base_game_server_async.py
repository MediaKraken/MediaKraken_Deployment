async def db_game_server_list(self, db_connection, offset=0, records=None):
    """
    Return game server list
    """
    return await db_connection.fetch('select mm_game_server_guid,'
                                     ' mm_game_server_name,'
                                     ' mm_game_server_json'
                                     ' from mm_game_dedicated_servers'
                                     ' order by mm_game_server_name offset $1 limit $2)',
                                     offset, records)
