import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_sync_progress_update(self, sync_guid, sync_percent, db_connection=None):
    """
    # update progress
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
    await db_conn.execute('update mm_sync set mm_sync_options_json->\'Progress\' = $1'
                          ' where mm_sync_guid = $2', sync_percent, sync_guid)
    await db_conn.execute('commit')


async def db_sync_list_count(self, db_connection=None):
    """
    # return count of sync jobs
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
    return await db_conn.fetchval('select count(*) from mm_sync')


async def db_sync_delete(self, sync_guid, db_connection=None):
    """
    # delete sync job
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
    await db_conn.execute(
        'delete from mm_sync'
        ' where mm_sync_guid = $1', sync_guid)


async def db_sync_insert(self, sync_path, sync_path_to, sync_json, db_connection=None):
    """
    # insert sync job
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
    await db_conn.execute('insert into mm_sync (mm_sync_guid,'
                          ' mm_sync_path,'
                          ' mm_sync_path_to,'
                          ' mm_sync_options_json)'
                          ' values ($1, $2, $3, $4)',
                          new_guid, sync_path,
                          sync_path_to, sync_json)
    return new_guid


async def db_sync_list(self, offset=0, records=None, user_guid=None, db_connection=None):
    """
    # return list of sync jobs
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
    # TODO by priority, name, year
    if user_guid is None:
        # complete list for admins
        return await db_conn.fetch('select mm_sync_guid uuid,'
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
                                   ' desc, mm_sync_path',
                                   offset, records)
    else:
        return await db_conn.fetch('select mm_sync_guid uuid,'
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
                                   ' desc, mm_sync_path',
                                   str(user_guid), offset, records)
