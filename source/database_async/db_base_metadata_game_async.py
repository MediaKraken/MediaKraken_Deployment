async def db_meta_game_by_guid(self, db_connection, guid):
    """
    # return game data
    """
    return await db_connection.fetchrow('select gi_id,'
                                        ' gi_system_id,'
                                        ' gi_game_info_json'
                                        ' from mm_metadata_game_software_info'
                                        ' where gi_id = $1', guid)


async def db_meta_game_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of games
    """
    if search_value is not None:
        return await db_connection.fetch('select gi_id,gi_game_info_short_name,'
                                         ' gi_game_info_name,'
                                         ' gi_game_info_json->\'year\','
                                         ' gs_game_system_json->\'description\''
                                         ' from mm_metadata_game_software_info,'
                                         ' mm_metadata_game_systems_info'
                                         ' where gi_system_id = gs_id and gi_game_info_name % $1'
                                         ' order by gi_game_info_name, gi_game_info_json->\'year\''
                                         ' offset $2 limit $3', search_value, offset, records)
    else:
        return await db_connection.fetch('select gi_id,gi_game_info_short_name,'
                                         ' gi_game_info_name,'
                                         ' gi_game_info_json->\'year\','
                                         ' gs_game_system_json->\'description\''
                                         ' from mm_metadata_game_software_info,'
                                         ' mm_metadata_game_systems_info'
                                         ' where gi_system_id = gs_id'
                                         ' order by gi_game_info_name,'
                                         ' gi_game_info_json->\'year\''
                                         ' offset $1 limit $2', offset, records)
