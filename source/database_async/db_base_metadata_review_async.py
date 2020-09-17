async def db_review_list_by_tmdb_guid(self, metadata_id, db_connection=None):
    """
    # grab reviews for metadata
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO order by release date
    # TODO order by rating? (optional?)
    return await self.db_connection.fetch('select mm_review_guid,'
                                          ' mm_review_json::json'
                                          ' from mm_review'
                                          ' where mm_review_metadata_id = $1',
                                          str(metadata_id))
