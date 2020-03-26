import uuid


async def db_download_insert(self, db_connection, provider, que_type, down_json):
    """
    Create/insert a download into the que
    """
    new_guid = str(uuid.uuid4())
    await db_connection.execute('insert into mm_download_que (mdq_id,'
                                'mdq_provider,'
                                'mdq_que_type,'
                                'mdq_download_json)'
                                ' values (%s,%s,%s,%s)',
                                (new_guid, provider, que_type, down_json))
    return new_guid
