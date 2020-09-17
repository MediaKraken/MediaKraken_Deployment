import uuid


async def db_opt_update(self, option_json, db_connection=None):
    """
    Update option json
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json::json = $1',
                          option_json)


async def db_opt_json_read(self, db_connection=None):
    """
    Read options
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval(
        'select mm_options_json::json'
        ' from mm_options_and_status')


async def db_opt_status_read(self, db_connection=None):
    """
    Read options, status
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow(
        'select mm_options_json::json, mm_status_json::json'
        ' from mm_options_and_status')


async def db_status_json_read(self, db_connection=None):
    """
    Read options
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval(
        'select mm_status_json::json'
        ' from mm_options_and_status')


async def db_opt_status_insert(self, option_json, status_json, db_connection=None):
    """
    insert status
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('insert into mm_options_and_status'
                          ' (mm_options_and_status_guid,'
                          ' mm_options_json::json,'
                          ' mm_status_json::json)'
                          ' values ($1,$2,$3)',
                          str(uuid.uuid4()), option_json, status_json)
    await db_conn.execute('commit')


async def db_opt_status_update(self, option_json, status_json, db_connection=None):
    """
    Update option and status json
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json::json = $1,'
                          ' mm_status_json::json = $2',
                          option_json, status_json)
    await db_conn.execute('commit')
