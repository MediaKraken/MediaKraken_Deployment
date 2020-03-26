async def db_meta_music_video_count(self, db_connection, imvdb_id=None, search_value=None):
    """
    Return count of music video metadata
    """
    if imvdb_id is None:
        if search_value is not None:
            return await db_connection.fetchval('select count(*) from mm_metadata_music_video'
                                                ' where mm_media_music_video_song %% %s',
                                                search_value)
        else:
            return await db_connection.fetchval(
                'select count(*) from mm_metadata_music_video')
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_music_video'
                                            ' where mm_metadata_music_video_media_id->\'imvdb\' ? %s',
                                            imvdb_id)


async def db_meta_music_video_detail_uuid(self, db_connection, item_guid):
    """
    Grab metadata for specified music video
    """
    return await db_connection.fetchrow('select mm_media_music_video_band,'
                                        ' mm_media_music_video_song,'
                                        ' mm_metadata_music_video_json,'
                                        ' mm_metadata_music_video_localimage_json'
                                        ' from mm_metadata_music_video'
                                        ' where mm_metadata_music_video_guid = %s', item_guid)


async def db_meta_music_video_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    List music video metadata
    """
    # TODO order by release date
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_music_video_guid,'
                                         ' mm_media_music_video_band,'
                                         ' mm_media_music_video_song,'
                                         ' mm_metadata_music_video_localimage_json'
                                         ' from mm_metadata_music_video'
                                         ' where mm_media_music_video_song %% %s '
                                         'order by LOWER(mm_media_music_video_band),'
                                         ' LOWER(mm_media_music_video_song)'
                                         ' offset %s limit %s',
                                         search_value, offset, records)
    else:
        return await db_connection.fetch('select mm_metadata_music_video_guid,'
                                         ' mm_media_music_video_band,'
                                         ' mm_media_music_video_song,'
                                         ' mm_metadata_music_video_localimage_json'
                                         ' from mm_metadata_music_video'
                                         ' order by LOWER(mm_media_music_video_band),'
                                         ' LOWER(mm_media_music_video_song) offset %s limit %s',
                                         offset, records)
