import uuid


async def db_notification_insert(self, db_connection, notification_data, notification_dismissable):
    """
    # insert notifications
    """
    new_guid = str(uuid.uuid4())
    await db_connection.execute('insert into mm_notification (mm_notification_guid,'
                                'mm_notification_text,'
                                'mm_notification_time,'
                                'mm_notification_dismissable)'
                                ' values ($1, $2, CURRENT_TIMESTAMP, $3)', new_guid,
                                notification_data,
                                notification_dismissable)
    return new_guid


async def db_notification_read(self, db_connection, offset=0, records=None):
    """
    # read all notifications
    """
    return await db_connection.fetch('select mm_notification_guid,'
                                     ' mm_notification_text,'
                                     ' mm_notification_time,'
                                     ' mm_notification_dismissable'
                                     ' from mm_notification'
                                     ' order by mm_notification_time desc offset $1 limit $2',
                                     offset, records)


async def db_notification_delete(self, db_connection, notification_uuid):
    """
    # remove notifications
    """
    await db_connection.execute('delete from mm_notification'
                                ' where mm_notification_guid = $1',
                                notification_uuid)
