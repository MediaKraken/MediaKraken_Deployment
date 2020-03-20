



def db_media_album_count(self, db_connection, search_value=None):
    """
    Album count
    """
    if search_value is not None:
        # this could possibly return null since search hence the try/catch below
        return db_connection.fetchval('select count(*) from mm_metadata_album, mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_album_guid '
                                      ' and mm_metadata_album_name %% %s'
                                      ' group by mm_metadata_album_guid',
                                      (search_value,))
    else:
        # this could possibly return null in the distinct hence the try/catch below
        return db_connection.fetchval('select count(*) from (select distinct mm_metadata_album_guid'
                                      ' from mm_metadata_album, mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_album_guid) as temp')


def db_media_album_list(self, db_connection, offset=0, per_page=None, search_value=None):
    """
    Album list
    """
    # TODO only grab the image part of the json for list
    if search_value is not None:
        return db_connection.fetch('select mm_metadata_album_guid,'
                                   'mm_metadata_album_name,'
                                   'mm_metadata_album_json'
                                   ' from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid'
                                   ' and mm_metadata_album_name %% %s'
                                   ' group by mm_metadata_album_guid'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset %s limit %s', (search_value, offset, per_page))
    else:
        return db_connection.fetch('select mm_metadata_album_guid,'
                                   'mm_metadata_album_name,'
                                   'mm_metadata_album_json'
                                   ' from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid'
                                   ' group by mm_metadata_album_guid'
                                   ' order by LOWER(mm_metadata_album_name)'
                                   ' offset %s limit %s', (offset, per_page))