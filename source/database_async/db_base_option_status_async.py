async def db_opt_update(self, option_json):
    """
    Update option json
    """
    # no need for where clause as it's only the one record
    await self.db_connection.execute('update mm_options_and_status'
                                     ' set mm_options_json = $1',
                                     option_json)


async def db_opt_json_read(self):
    """
    Read options
    """
    return await self.db_connection.fetchval(
        'SELECT row_to_json(json_data)'
        ' FROM(select mm_options_json'
        ' from mm_options_and_status) as json_data')


async def db_opt_status_read(self):
    """
    Read options, status
    """
    return await self.db_connection.fetchrow(
        'SELECT row_to_json(json_data)'
        ' FROM(select mm_options_json, mm_status_json'
        ' from mm_options_and_status) as json_data')


async def db_status_json_read(self):
    """
    Read options
    """
    return await self.db_connection.fetchval(
        'SELECT row_to_json(json_data)'
        ' FROM(select mm_status_json'
        ' from mm_options_and_status) as json_data')
