async def db_notification_read(db_connection, offset=0, records=None):
    """
    # read all notifications
    """
    return await db_connection.fetch('select mm_notification_guid,'
                                     ' mm_notification_text,'
                                     ' mm_notification_time,'
                                     ' mm_notification_dismissable'
                                     ' from mm_notification'
                                     ' order by mm_notification_time desc'
                                     ' offset $1 limit $2',
                                     offset, records)
