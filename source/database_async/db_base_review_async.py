import uuid


async def db_review_count(self, metadata_id):
    """
    # count reviews for media
    """
    return await self.db_connection.fetchval('select count(*) from mm_review'
                                             ' where mm_review_metadata_guid = $1',
                                             metadata_id)


async def db_review_list_by_tmdb_guid(self, metadata_id):
    """
    # grab reviews for metadata
    """
    # TODO order by release date
    # TODO order by rating? (optional?)
    return await self.db_connection.fetch('select mm_review_guid,'
                                          'mm_review_json'
                                          ' from mm_review'
                                          ' where mm_review_metadata_id->\'themoviedb\' ? $1',
                                          metadata_id)


async def db_review_insert(self, metadata_id, review_json):
    """
    # insert record
    """
    new_guid = str(uuid.uuid4())
    await self.db_cursor.execute('insert into mm_review (mm_review_guid,'
                                 ' mm_review_metadata_id,'
                                 ' mm_review_json)'
                                 ' values ($1,$2,$3)',
                                 new_guid, metadata_id, review_json)
    await self.db_cursor.db_commit()
    return new_guid
