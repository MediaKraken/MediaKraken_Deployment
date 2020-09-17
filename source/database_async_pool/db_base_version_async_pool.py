async def db_version_check(self, db_connection):
    """
    query db version
    """
    return db_connection.fetchval('select mm_version_no'
                                  ' from mm_version')
