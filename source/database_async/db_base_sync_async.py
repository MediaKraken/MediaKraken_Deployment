import uuid


async def db_sync_progress_update(self, sync_guid, sync_percent):
    """
    # update progress
    """
    await self.db_connection.execute('update mm_sync set mm_sync_options_json->\'Progress\' = $1'
                                     ' where mm_sync_guid = $2', sync_percent, sync_guid)
    await self.db_connection.execute('commit')


async def db_sync_list_count(self):
    """
    # return count of sync jobs
    """
    return await self.db_connection.fetchval('select count(*) from mm_sync')


async def db_sync_delete(self, sync_guid):
    """
    # delete sync job
    """
    await self.db_connection.execute(
        'delete from mm_sync'
        ' where mm_sync_guid = $1', sync_guid)


async def db_sync_insert(self, sync_path, sync_path_to, sync_json):
    """
    # insert sync job
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_sync (mm_sync_guid,'
                                     ' mm_sync_path,'
                                     ' mm_sync_path_to,'
                                     ' mm_sync_options_json)'
                                     ' values ($1, $2, $3, $4)',
                                     new_guid, sync_path,
                                     sync_path_to, sync_json)
    return new_guid


async def db_sync_list(self, offset=0, records=None, user_guid=None):
    """
    # return list of sync jobs
    """
    # TODO by priority, name, year
    if user_guid is None:
        # complete list for admins
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_sync_guid uuid,'
                                              ' mm_sync_path,'
                                              ' mm_sync_path_to,'
                                              ' mm_sync_options_json'
                                              ' from mm_sync'
                                              ' where mm_sync_guid in (select mm_sync_guid'
                                              ' from mm_sync'
                                              ' order by mm_sync_options_json->\'Priority\''
                                              ' desc, mm_sync_path'
                                              ' offset $1 limit $2)'
                                              ' order by mm_sync_options_json->\'Priority\''
                                              ' desc, mm_sync_path) as json_data',
                                              offset, records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_sync_guid uuid,'
                                              ' mm_sync_path,'
                                              ' mm_sync_path_to,'
                                              ' mm_sync_options_json'
                                              ' from mm_sync'
                                              ' where mm_sync_guid in (select mm_sync_guid'
                                              ' from mm_sync'
                                              ' where mm_sync_options_json->\'User\'::text = $1'
                                              ' order by mm_sync_options_json->\'Priority\''
                                              ' desc, mm_sync_path offset $2 limit $3)'
                                              ' order by mm_sync_options_json->\'Priority\''
                                              ' desc, mm_sync_path) as json_data',
                                              str(user_guid), offset, records)
