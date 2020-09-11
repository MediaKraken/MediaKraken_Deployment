import datetime
import uuid


async def db_cron_delete(self, cron_uuid):
    """
    Delete cron job
    """
    await self.db_connection.execute('delete from mm_cron'
                                     ' where mm_cron_guid = $1',
                                     cron_uuid)


async def db_cron_info(self, cron_uuid):
    """
    Cron job info
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_cron_guid,'
                                             ' mm_cron_name,'
                                             ' mm_cron_description,'
                                             ' mm_cron_enabled,'
                                             ' mm_cron_schedule,'
                                             ' mm_cron_last_run,'
                                             ' mm_cron_json'
                                             ' from mm_cron'
                                             ' where mm_cron_guid = $1)'
                                             ' as json_data', cron_uuid)


async def db_cron_insert(self, cron_name, cron_desc, cron_enabled,
                         cron_schedule, cron_last_run, cron_json):
    """
    insert cron job
    """
    new_cron_id = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_cron (mm_cron_guid,'
                                     ' mm_cron_name,'
                                     ' mm_cron_description,'
                                     ' mm_cron_enabled,'
                                     ' mm_cron_schedule,'
                                     ' mm_cron_last_run, mm_cron_json)'
                                     ' values ($1,$2,$3,$4,$5,$6,$7)',
                                     new_cron_id, cron_name, cron_desc,
                                     cron_enabled, cron_schedule,
                                     cron_last_run, cron_json)
    return new_cron_id


async def db_cron_list(self, enabled_only=False, offset=0, records=None):
    """
    Return cron list
    """
    if not enabled_only:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_cron_guid,'
                                              ' mm_cron_name,'
                                              ' mm_cron_description,'
                                              ' mm_cron_enabled,'
                                              ' mm_cron_schedule,'
                                              ' mm_cron_last_run,'
                                              ' mm_cron_json'
                                              ' from mm_cron where mm_cron_guid'
                                              ' in (select mm_cron_guid from mm_cron'
                                              ' order by mm_cron_name offset $1 limit $2)'
                                              ' order by mm_cron_name)'
                                              ' as json_data', offset,
                                              records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_cron_guid,'
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
                                              ' order by mm_cron_name) as json_data', offset,
                                              records)


async def db_cron_list_count(self, enabled_only=False):
    """
    Return number of cron jobs
    """
    if not enabled_only:
        return await self.db_connection.fetchval('select count(*) from mm_cron')
    else:
        return await self.db_connection.fetchval('select count(*) from mm_cron'
                                                 ' where mm_cron_enabled = true')


async def db_cron_time_update(self, cron_type):
    """
    Update the datetime in which a cron job was run
    """
    await self.db_connection.execute('update mm_cron set mm_cron_last_run = $1'
                                     ' where mm_cron_name = $2',
                                     datetime.datetime.now(), cron_type)
