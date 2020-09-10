import uuid

from common import common_global


async def db_download_insert(self, provider, que_type, down_json):
    """
    Create/insert a download into the que
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_download_que (mdq_id,'
                                     'mdq_provider,'
                                     'mdq_que_type,'
                                     'mdq_download_json)'
                                     ' values ($1, $2, $3, $4)',
                                     new_guid, provider, que_type, down_json)
    return new_guid


async def db_download_read_provider(self, provider_name):
    """
    Read the downloads by provider
    """
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select mdq_id,'
                                          ' mdq_que_type,'
                                          ' mdq_download_json'
                                          ' from mm_download_que'
                                          ' where mdq_provider = $1'
                                          ' order by mdq_que_type limit 25)'
                                          ' as json_data',
                                          provider_name)


async def db_download_delete(self, guid):
    """
    Remove download
    """
    self.db_connection.execute('delete from mm_download_que'
                               ' where mdq_id = $1', guid)
    self.db_connection.db_commit()


async def db_download_update_provider(self, provider_name, guid):
    """
    Update provider
    """
    common_global.es_inst.com_elastic_index('info', {'download update provider': provider_name,
                                                     'guid': guid})
    self.db_connection.execute('update mm_download_que set mdq_provider = $1 where mdq_id = $2',
                               provider_name, guid)


async def db_download_update(self, update_json, guid, update_que_id=None):
    """
    Update download que record
    """
    common_global.es_inst.com_elastic_index('info', {'download update': update_json,
                                                     'que': update_que_id, 'guid': guid})
    if update_que_id is not None:
        self.db_connection.execute('update mm_download_que set mdq_download_json = $1,'
                                   ' mdq_que_type = $2'
                                   ' where mdq_id = $3',
                                   update_json, update_que_id, guid)
    else:
        self.db_connection.execute('update mm_download_que set mdq_download_json = $1'
                                   ' where mdq_id = $2', (update_json, guid))


async def db_download_que_exists(self, download_que_uuid, download_que_type,
                                 provider_name, provider_id):
    """
    See if download que record exists for provider and id and type
        still need this as records could be from different threads or not in order
        and themoviedb "reuses" media id records for tv/movie
    """
    # include search to find OTHER records besides the row that's
    # doing the query itself
    # this should now catch anything that's Fetch+, there should also technically
    # only ever be one Fetch+, rest should be search or null
    common_global.es_inst.com_elastic_index('info', {'db_download_que_exists': download_que_uuid,
                                                     'name': provider_name,
                                                     'id': provider_id})
    # que type is movie, tv, etc as those numbers could be reused
    self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                ' FROM (select mdq_download_json->\'MetaNewID\''
                                ' from mm_download_que'
                                ' where mdq_provider = $1 and mdq_que_type = $2'
                                ' and mdq_download_json->\'ProviderMetaID\' ? $3 limit 1)'
                                ' as json_data',
                                provider_name, download_que_type, provider_id)
