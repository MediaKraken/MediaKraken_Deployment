async def db_meta_game_system_by_guid(self, guid, db_connection=None):
    """
    # return game system data
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow('select * from mm_metadata_game_systems_info'
                                  ' where gs_id = $1',
                                  guid)


async def db_meta_game_system_list_count(self, search_value=None, db_connection=None):
    """
    Return game system count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetchval(
            'select count(*) from mm_metadata_game_systems_info'
            ' where gs_game_system_json->\'@isdevice\' ? \'yes\''
            ' and gs_game_system_name % $1', search_value)
    else:
        return await db_conn.fetchval(
            'select count(*) from mm_metadata_game_systems_info'
            ' where gs_game_system_json->\'@isdevice\' ? \'yes\'')


async def db_meta_game_system_list(self, offset=0, records=None, search_value=None,
                                   db_connection=None):
    """
    # return list of game systems
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO might need to sort by release year as well for machines with multiple releases
    if search_value is not None:
        return await db_conn.fetch('select gs_id,gs_game_system_name,'
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_id in (select gs_id'
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' and gs_game_system_name % $1 '
                                   'order by gs_game_system_json->\'description\''
                                   ' offset $2 limit $2)'
                                   ' order by gs_game_system_json->\'description\'',
                                   search_value, offset, records)
    else:
        return await db_conn.fetch('select gs_id,gs_game_system_name,'
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_id in (select gs_id'
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' '
                                   'order by gs_game_system_json->\'description\''
                                   ' offset $1 limit $2)'
                                   ' order by gs_game_system_json->\'description\'',
                                   offset, records)
