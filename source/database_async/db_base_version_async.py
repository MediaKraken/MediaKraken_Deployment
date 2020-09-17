async def db_version_check(self, db_connection=None):
    """
    query db version
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return self.db_connection.fetchval('select mm_version_no'
                                       ' from mm_version')


async def db_version_update(self, version_no, db_connection=None):
    """
    update db version
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_connection.execute(
        'update mm_version set mm_version_no = $1', version_no)
