
async def db_cron_delete(self, cron_uuid, db_connection=None):
    """
    Delete cron job
    """
    await db_conn.execute('delete from mm_cron'
                          ' where mm_cron_guid = $1',
                          cron_uuid)


async def db_cron_info(self, cron_uuid, db_connection=None):
    """
    Cron job info
    """
    return await db_conn.fetchrow('select mm_cron_guid,'
                                  ' mm_cron_name,'
                                  ' mm_cron_description,'
                                  ' mm_cron_enabled,'
                                  ' mm_cron_schedule,'
                                  ' mm_cron_last_run,'
                                  ' mm_cron_json'
                                  ' from mm_cron'
                                  ' where mm_cron_guid = $1', cron_uuid)


async def db_cron_insert(self, cron_name, cron_desc, cron_enabled,
                         cron_schedule, cron_last_run, cron_json, db_connection=None):
    """
    insert cron job
    """
    new_cron_id = uuid.uuid4()
    await db_conn.execute('insert into mm_cron (mm_cron_guid,'
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


async def db_cron_list(self, enabled_only=False, offset=0, records=None, db_connection=None):
    """
    Return cron list
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if not enabled_only:
        return await db_conn.fetch('select mm_cron_guid,'
                                   ' mm_cron_name,'
                                   ' mm_cron_description,'
                                   ' mm_cron_enabled,'
                                   ' mm_cron_schedule,'
                                   ' mm_cron_last_run,'
                                   ' mm_cron_json'
                                   ' from mm_cron where mm_cron_guid'
                                   ' in (select mm_cron_guid from mm_cron'
                                   ' order by mm_cron_name offset $1 limit $2)'
                                   ' order by mm_cron_name', offset,
                                   records)
    else:
        return await db_conn.fetch('select mm_cron_guid,'
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
                                   ' order by mm_cron_name', offset,
                                   records)


async def db_cron_list_count(self, enabled_only=False, db_connection=None):
    """
    Return number of cron jobs
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if not enabled_only:
        return await db_conn.fetchval('select count(*) from mm_cron')
    else:
        return await db_conn.fetchval('select count(*) from mm_cron'
                                      ' where mm_cron_enabled = true')


async def db_cron_time_update(self, cron_type, db_connection=None):
    """
    Update the datetime in which a cron job was run
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('update mm_cron set mm_cron_last_run = $1'
                          ' where mm_cron_name = $2',
                          datetime.datetime.now(), cron_type)
