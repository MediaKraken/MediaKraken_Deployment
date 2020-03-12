def db_meta_game_by_guid(self, db_connection, guid):
    """
    # return game data
    """
    return db_connection.fetch('select gi_id,'
                               ' gi_system_id,'
                               ' gi_game_info_json'
                               ' from mm_metadata_game_software_info'
                               ' where gi_id = %s', (guid,))
