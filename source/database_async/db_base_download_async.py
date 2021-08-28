
async def db_download_insert(self, provider, que_type, down_json, down_new_uuid,
                             db_connection=None):
    """
    Create/insert a download into the que
    """
    await db_conn.execute('insert into mm_download_que (mdq_id,'
                          ' mdq_provider,'
                          ' mdq_que_type,'
                          ' mdq_new_uuid,'
                          ' mdq_provider_id,'
                          ' mdq_status)'
                          ' values ($1, $2, $3, $4, $5, $6)',
                          new_guid, provider, que_type, down_new_uuid,
                          down_json['ProviderMetaID'], down_json['Status'])
    return new_guid


async def db_download_update_provider(self, provider_name, guid, db_connection=None):
    """
    Update provider
    """
    await db_conn.execute('update mm_download_que set mdq_provider = $1 where mdq_id = $2',
                          provider_name, guid)


async def db_download_update(self, guid, status, provider_guid=None, db_connection=None):
    """
    Update download que record
    """
    if provider_guid is not None:
        await db_conn.execute('update mm_download_que set mdq_status = $1,'
                              ' mdq_provider_id = $2'
                              ' where mdq_id = $3',
                              status, provider_guid, guid)
    else:
        await db_conn.execute('update mm_download_que set mdq_status = $1'
                              ' where mdq_id = $2', status, guid)
