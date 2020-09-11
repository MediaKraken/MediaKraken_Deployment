async def db_version_check(self):
    """
    query db version
    """
    return self.db_connection.fetchval('select mm_version_no'
                                       ' from mm_version')


async def db_version_update(self, version_no):
    """
    update db version
    """
    self.db_connection.execute(
        'update mm_version set mm_version_no = $1', version_no)
