async def db_meta_game_by_guid(self, guid, db_connection=None):
    """
    # return game data
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow('select gi_id,'
                                  ' gi_system_id,'
                                  ' gi_game_info_json::json'
                                  ' from mm_metadata_game_software_info'
                                  ' where gi_id = $1', guid)


async def db_meta_game_by_sha1(self, sha1_hash, db_connection=None):
    """
    # return game uuid by sha1 hash
    """
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
