import uuid


async def db_opt_update(self, option_json):
    """
    Update option json
    """
    # no need for where clause as it's only the one record
    await self.db_connection.execute('update mm_options_and_status'
                                     ' set mm_options_json::json = $1',
                                     option_json)


async def db_opt_json_read(self):
    """
    Read options
    """
    return await self.db_connection.fetchval(
        'select mm_options_json::json'
        ' from mm_options_and_status')


async def db_opt_status_read(self):
    """
    Read options, status
    """
    return await self.db_connection.fetchrow(
        'select mm_options_json::json, mm_status_json::json'
        ' from mm_options_and_status')


async def db_status_json_read(self):
    """
    Read options
    """
    return await self.db_connection.fetchval(
        'select mm_status_json::json'
        ' from mm_options_and_status')


async def db_opt_status_insert(self, option_json, status_json):
    """
    insert status
    """
    await self.db_connection.execute('insert into mm_options_and_status'
                                     ' (mm_options_and_status_guid,'
                                     ' mm_options_json::json,'
                                     ' mm_status_json::json)'
                                     ' values ($1,$2,$3)',
                                     str(uuid.uuid4()), option_json, status_json)
    await self.db_connection.execute('commit')


async def db_opt_status_update(self, option_json, status_json):
    """
    Update option and status json
    """
    # no need for where clause as it's only the one record
    await self.db_connection.execute('update mm_options_and_status'
                                     ' set mm_options_json::json = $1,'
                                     ' mm_status_json::json = $2',
                                     option_json, status_json)
    await self.db_connection.execute('commit')
