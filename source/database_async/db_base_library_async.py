import datetime
import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_library_path_add(self, dir_path, class_guid, share_guid, db_connection=None):
    """
    # add media path
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
    await db_conn.execute('insert into mm_media_dir (mm_media_dir_guid,'
                          ' mm_media_dir_path,'
                          ' mm_media_dir_class_type,'
                          ' mm_media_dir_last_scanned)'
                          ' values ($1, $2, $3, $4, $5)',
                          new_guid, dir_path, class_guid,
                          datetime.datetime(1970, 1, 1, 0, 0, 1), share_guid)
    return new_guid


async def db_library_path_by_uuid(self, dir_id, db_connection=None):
    """
    # lib data per id
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
    return await db_conn.fetchrow('select mm_media_dir_path,'
                                  ' mm_media_dir_class_type'
                                  ' from mm_media_dir'
                                  ' where mm_media_dir_guid = $1',
                                  dir_id)


async def db_library_path_check(self, dir_path, db_connection=None):
    """
    # lib path check (dupes)
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
    return await db_conn.fetchval(
        'select count(*) from mm_media_dir where mm_media_dir_path = $1',
        dir_path)


async def db_library_path_delete(self, lib_guid, db_connection=None):
    """
    # remove media path
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
        'delete from mm_media_dir where mm_media_dir_guid = $1', lib_guid)


async def db_library_path_status(self, db_connection=None):
    """
    # read scan status
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
    return await db_conn.fetch('select mm_media_dir_path,'
                               ' mm_media_dir_status'
                               ' from mm_media_dir'
                               ' where mm_media_dir_status IS NOT NULL'
                               ' order by mm_media_dir_path')


async def db_library_path_update_by_uuid(self, lib_path, class_guid, lib_guid, db_connection=None):
    """
    # update audit path
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
    await db_conn.execute('update mm_media_dir set mm_media_dir_path = $1,'
                          ' mm_media_dir_class_type = $2'
                          ' where mm_media_dir_guid = $3',
                          lib_path, class_guid, lib_guid)


async def db_library_paths(self, offset=0, records=None, db_connection=None):
    """
    # read the paths to audit
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
    return await db_conn.fetch('select mm_media_dir_guid,'
                               ' mm_media_dir_path,'
                               ' mm_media_dir_class_type,'
                               ' mm_media_dir_last_scanned'
                               ' from mm_media_dir'
                               ' order by mm_media_dir_class_type, mm_media_dir_path'
                               ' offset $1 limit $2', offset, records)
