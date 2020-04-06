async def db_meta_queue_list_count(self, db_connection, user_id, search_value=None):
    """
    Return count of queued media for user
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*)'
                                            ' from mm_user_queue where mm_user_queue_name = $1'
                                            ' and mm_user_queue_user_id = $2',
                                            search_value, user_id)
    else:
        return await db_connection.fetchval('select count(*) from mm_user_queue'
                                            'where mm_user_queue_user_id = $1', user_id)

# TODO create table!
"""
mm_user_queue

mm_user_queue_id = uuid
mm_user_queue_name = text
mm_user_queue_user_id = uuid
mm_user_queue_media_type = int
mm_user_queue_media_guid = uuid
"""
