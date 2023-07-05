
async def db_extension_available(self, db_connection=None):
    """
    list available extensions
    """
    return await db_conn.fetch('SELECT * FROM pg_available_extensions')


async def db_extension_installed(self, db_connection=None):
    """
    list installed extensions
    """
    return await db_conn.fetch('SELECT * FROM pg_extension')
