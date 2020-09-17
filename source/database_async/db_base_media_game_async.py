async def db_media_game_system_list_count(self, search_value=None, db_connection=None):
    """
    Audited system list count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_game_system_list(self, offset=0, records=None, search_value=None,
                                    db_connection=None):
    """
    Audited system list
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_game_list_by_system_count(self, system_id, search_value=None,
                                             db_connection=None):
    """
    Audited game list by system count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_game_list_by_system(self, system_id, offset=0, records=None, search_value=None,
                                       db_connection=None):
    """
    Audited game list by system
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_game_list_count(self, search_value=None, db_connection=None):
    """
    Audited games list count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_game_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    Audited games list
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass


async def db_media_mame_game_list(self, db_connection=None):
    """
    Game systems are NULL for MAME
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await self.db_connection.fetch('select gi_id, gi_short_name'
                                   ' from mm_game_info'
                                   ' where gi_system_id is null'
                                   ' and gi_gc_category is null')


async def db_media_game_category_update(self, category, game_id, db_connection=None):
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await self.db_connection.execute('update mm_game_info'
                                     ' set gi_gc_category = $1'
                                     ' where gi_id = $2', category, game_id)
    await self.db_connection.execute('commit')


async def db_media_game_clone_list(self, db_connection=None):
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetch('select gi_id,'
                                          ' gi_cloneof'
                                          ' from mm_game_info'
                                          ' where gi_system_id is null'
                                          ' and gi_cloneof IS NOT NULL'
                                          ' and gi_gc_category is null')


async def db_media_game_category_by_name(self, category_name, db_connection=None):
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await self.db_connection.fetchval('select gi_gc_category'
                                      ' from mm_game_info'
                                      ' where gi_short_name = $1', category_name)
