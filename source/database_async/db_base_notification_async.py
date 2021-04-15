import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_notification_insert(self, notification_data, notification_dismissable,
                                 db_connection=None):
    """
    # insert notifications
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
    await db_conn.execute('insert into mm_notification (mm_notification_guid,'
                          'mm_notification_text,'
                          'mm_notification_time,'
                          'mm_notification_dismissable)'
                          ' values ($1, $2, CURRENT_TIMESTAMP, $3)', new_guid,
                          notification_data,
                          notification_dismissable)
    return new_guid


async def db_notification_read(self, offset=0, records=None, db_connection=None):
    """
    # read all notifications
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
    return await db_conn.fetch('select mm_notification_guid,'
                               ' mm_notification_text,'
                               ' mm_notification_time,'
                               ' mm_notification_dismissable'
                               ' from mm_notification'
                               ' order by mm_notification_time desc'
                               ' offset $1 limit $2',
                               offset, records)


async def db_notification_delete(self, notification_uuid, db_connection=None):
    """
    # remove notifications
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
    await db_conn.execute('delete from mm_notification'
                          ' where mm_notification_guid = $1',
                          notification_uuid)
