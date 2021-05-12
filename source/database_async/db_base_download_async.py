import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_download_insert(self, provider, que_type, down_json, down_new_uuid,
                             db_connection=None):
    """
    Create/insert a download into the que
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
    new_guid = uuid.uuid4()
    await db_conn.execute('insert into mm_download_que (mdq_id,'
                          ' mdq_provider,'
                          ' mdq_que_type,'
                          ' mdq_new_uuid,'
                          ' mdq_provider_id,'
                          ' mdq_status)'
                          ' values ($1, $2, $3, $4, $5, $6)',
                          new_guid, provider, que_type, down_new_uuid,
                          down_json['MediaID']. down_json['ProviderMetaID'])
    return new_guid


async def db_download_read_provider(self, provider_name, db_connection=None):
    """
    Read the downloads by provider
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
    return await db_conn.fetch('select mdq_id,'
                               ' mdq_que_type,'
                               ' mdq_new_uuid,'
                               ' mdq_provider_id,'
                               ' mdq_status'
                               ' from mm_download_que'
                               ' where mdq_provider = $1'
                               ' order by mdq_que_type limit 25',
                               provider_name)


async def db_download_delete(self, guid, db_connection=None):
    """
    Remove download
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
    await db_conn.execute('delete from mm_download_que'
                          ' where mdq_id = $1', str(guid))


async def db_download_update_provider(self, provider_name, guid, db_connection=None):
    """
    Update provider
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
    await db_conn.execute('update mm_download_que set mdq_provider = $1 where mdq_id = $2',
                          provider_name, guid)


async def db_download_update(self, guid, status, provider_guid=None, db_connection=None):
    """
    Update download que record
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
    if provider_guid is not None:
        await db_conn.execute('update mm_download_que set mdq_status = $1,'
                              ' mdq_provider_id = $2'
                              ' where mdq_id = $3',
                              status, provider_guid, guid)
    else:
        await db_conn.execute('update mm_download_que set mdq_status = $1'
                              ' where mdq_id = $2', status, guid)


async def db_download_que_exists(self, download_que_uuid, download_que_type,
                                 provider_name, provider_id, db_connection=None,
                                 exists_only=False):
    """
    See if download que record exists for provider and id and type
        still need this as records could be from different threads or not in order
        and themoviedb "reuses" media id records for tv/movie
    """
    # include search to find OTHER records besides the row that's
    # doing the query itself
    # this should now catch anything that's Fetch+, there should also technically
    # only ever be one Fetch+, rest should be search or null
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
    # que type is movie, tv, etc as those numbers could be reused
    if exists_only:
        return await db_conn.fetchval('select exists(select 1'
                                      ' from mm_download_que'
                                      ' where mdq_provider = $1'
                                      ' and mdq_que_type = $2'
                                      ' and mdq_provider_id = $3'
                                      ' limit 1) limit 1',
                                      provider_name, download_que_type, provider_id)
    else:
        return await db_conn.fetchval('select mdq_new_uuid'
                                      ' from mm_download_que'
                                      ' where mdq_provider = $1'
                                      ' and mdq_que_type = $2'
                                      ' and mdq_provider_id = $3 limit 1',
                                      provider_name, download_que_type, provider_id)
