async def db_music_video_list(self, offset=0, per_page=None, search_value=None, db_connection=None):
    """
    music video list
    """
    pass


async def db_music_video_list_count(self, search_value=None, db_connection=None):
    """
    Music video count
    """
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_music_video, mm_media'
                                                 ' where mm_media_metadata_guid'
                                                 ' = mm_metadata_music_video_guid group'
                                                 ' and mm_media_music_video_song % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_music_video, mm_media'
                                                 ' where mm_media_metadata_guid'
                                                 ' = mm_metadata_music_video_guid')
