import datetime


def db_media_new(db_connection, days_old=7):
    return db_connection.fetchval('select count(*)'
                                  ' from mm_media, mm_metadata_movie'
                                  ' where mm_media_metadata_guid = mm_metadata_guid'
                                  ' and mm_media_json->>\'DateAdded\' >= %s',
                                  ((datetime.datetime.now()
                                    - datetime.timedelta(days=days_old)).strftime(
                                      "%Y-%m-%d"),))
