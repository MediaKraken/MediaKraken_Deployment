async def db_opt_json_read(db_connection):
    """
    Read options
    """
    return await db_connection.fetchval(
        'select mm_options_json::json'
        ' from mm_options_and_status')


async def db_opt_status_read(db_connection):
    """
    Read options, status
    """
    return await db_connection.fetchrow(
        'select mm_options_json::json, mm_status_json::json'
        ' from mm_options_and_status')


async def db_status_json_read(db_connection):
    """
    Read options
    """
    return await db_connection.fetchval(
        'select mm_status_json::json'
        ' from mm_options_and_status')
