import datetime
import json


def db_media_new(db_connection, days_old=7):
    return db_connection.fetchval('select count(*)'
                                  ' from mm_media, mm_metadata_movie'
                                  ' where mm_media_metadata_guid = mm_metadata_guid'
                                  ' and mm_media_json->>\'DateAdded\' >= %s',
                                  ((datetime.datetime.now()
                                    - datetime.timedelta(days=days_old)).strftime(
                                      "%Y-%m-%d"),))


def db_media_path_by_uuid(db_connection, media_uuid):
    """
    # find path for media by uuid
    """
    return db_connection.fetchval('select mm_media_path from mm_media'
                                  ' where mm_media_guid = %s',
                                  (media_uuid,))


def db_media_rating_update(db_connection, media_guid, user_id, status_text):
    """
    # set favorite status for media
    """
    if status_text == 'watched' or status_text == 'mismatch':
        status_setting = True
    else:
        status_setting = status_text
        status_text = 'Rating'
    try:
        json_data = db_connection.fetchval('SELECT mm_media_json from mm_media'
                                           ' where mm_media_guid = %s FOR UPDATE', (media_guid,))
        if 'UserStats' not in json_data:
            json_data['UserStats'] = {}
        if user_id in json_data['UserStats']:
            json_data['UserStats'][user_id][status_text] = status_setting
        else:
            json_data['UserStats'][user_id] = {status_text: status_setting}
        # TODO since 'for update' must release record on fail
        self.db_update_media_json(db_connection, media_guid, json.dumps(json_data))
        self.db_commit()
    except:
        self.db_rollback()
        return None
