async def db_version_check(self, db_connection=None):
    """
    query db version
    """
    return self.db_connection.fetchval('select mm_version_no'
                                       ' from mm_version')


async def db_version_update(self, version_no, db_connection=None):
    """
    update db version
    """
    self.db_connection.execute(
        'update mm_version set mm_version_no = $1', version_no)
