import datetime


async def db_cron_delete(self, db_connection, cron_uuid):
    """
    Delete cron job
    """
    await db_connection.execute('delete from mm_cron'
                                ' where mm_cron_guid = $1',
                                (cron_uuid,))


async def db_cron_info(self, db_connection, cron_uuid):
    """
    Cron job info
    """
    return await db_connection.fetchrow('select mm_cron_guid,'
                                        ' mm_cron_name,'
                                        ' mm_cron_description,'
                                        ' mm_cron_enabled,'
                                        ' mm_cron_schedule,'
                                        ' mm_cron_last_run,'
                                        ' mm_cron_json'
                                        ' from mm_cron'
                                        ' where mm_cron_guid = $1', (cron_uuid,))


async def db_cron_list(self, db_connection, enabled_only=False, offset=0, records=None):
    """
    Return cron list
    """
    if not enabled_only:
        return await db_connection.fetch('select mm_cron_guid,'
                                         ' mm_cron_name,'
                                         ' mm_cron_description,'
                                         ' mm_cron_enabled,'
                                         ' mm_cron_schedule,'
                                         ' mm_cron_last_run,'
                                         ' mm_cron_json'
                                         ' from mm_cron where mm_cron_guid'
                                         ' in (select mm_cron_guid from mm_cron'
                                         ' order by mm_cron_name offset $1 limit $2)'
                                         ' order by mm_cron_name', (offset, records))
    else:
        return await db_connection.fetch('select mm_cron_guid,'
                                         ' mm_cron_name,'
                                         ' mm_cron_description,'
                                         ' mm_cron_enabled,'
                                         ' mm_cron_schedule,'
                                         ' mm_cron_last_run,'
                                         ' mm_cron_json'
                                         ' from mm_cron where mm_cron_guid'
                                         ' in (select mm_cron_guid from mm_cron'
                                         ' where mm_cron_enabled = true'
                                         ' order by mm_cron_name offset $1 limit $2)'
                                         ' order by mm_cron_name', (offset, records))


async def db_cron_list_count(self, db_connection, enabled_only=False):
    """
    Return number of cron jobs
    """
    if not enabled_only:
        return await db_connection.fetchval('select count(*) from mm_cron')
    else:
        return await db_connection.fetchval(
            'select count(*) from mm_cron'
            ' where mm_cron_enabled = true')


async def db_cron_time_update(self, db_connection, cron_type):
    """
    Update the datetime in which a cron job was run
    """
    await db_connection.execute('update mm_cron set mm_cron_last_run = $1'
                                ' where mm_cron_name = $2',
                                (datetime.datetime.now(), cron_type))
