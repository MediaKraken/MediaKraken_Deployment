def db_music_video_list(self, db_connection, offset=0, per_page=None, search_value=None):
    """
    music video list
    """
    pass


def db_music_video_list_count(self, db_connection, search_value=None):
    """
    Music video count
    """
    if search_value is not None:
        return db_connection.fetchval('select count(*)'
                                      ' from mm_metadata_music_video, mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_music_video_guid group'
                                      ' and mm_media_music_video_song %% %s', (search_value,))
    else:
        return db_connection.fetchval('select count(*)'
                                      ' from mm_metadata_music_video, mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_music_video_guid')
