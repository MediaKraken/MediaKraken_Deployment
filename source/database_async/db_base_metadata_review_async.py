async def db_review_list_by_tmdb_guid(self, db_connection, metadata_id):
    """
    # grab reviews for metadata
    """
    # TODO order by release date
    # TODO order by rating? (optional?)
    return await db_connection.fetch('select mm_review_guid,'
                                     'mm_review_json'
                                     ' from mm_review'
                                     ' where mm_review_metadata_id = $1',
                                     str(metadata_id))
