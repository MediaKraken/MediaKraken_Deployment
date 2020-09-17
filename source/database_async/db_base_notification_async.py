import uuid


async def db_notification_insert(self, notification_data, notification_dismissable,
                                 db_connection=None):
    """
    # insert notifications
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_notification (mm_notification_guid,'
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
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetch('select mm_notification_guid,'
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
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await self.db_connection.execute('delete from mm_notification'
                                     ' where mm_notification_guid = $1',
                                     notification_uuid)
