import datetime
import inspect
import json

from common import common_logging_elasticsearch_httpx


async def db_media_duplicate(self, offset=0, records=None, db_connection=None):
    """
    # list duplicates
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO technically this will "dupe" things like subtitles atm, so group by class guid?
    return await db_conn.fetch('select mm_media_metadata_guid,'
                               ' mm_media_name,'
                               ' count(*)'
                               ' from mm_media, mm_metadata_movie'
                               ' where mm_media_metadata_guid is not null'
                               ' and mm_media_metadata_guid = mm_metadata_guid'
                               ' group by mm_media_metadata_guid,'
                               ' mm_media_name HAVING count(*) > 1'
                               ' order by LOWER(mm_media_name)'
                               ' offset $1 limit $2',
                               offset, records)


async def db_media_duplicate_count(self, db_connection=None):
    """
    # count the duplicates for pagination
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO technically this will "dupe" things like subtitles atm
    # TODO perhaps group by classid?
    return await db_conn.fetchval('select count(*) from (select mm_media_metadata_guid'
                                  ' from mm_media'
                                  ' where mm_media_metadata_guid is not null'
                                  ' group by mm_media_metadata_guid'
                                  ' HAVING count(*) > 1) as total')


async def db_media_duplicate_detail(self, guid, offset=0, records=None, db_connection=None):
    """
    # list duplicate detail
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetch('select mm_media_guid,'
                               'mm_media_path,'
                               'mm_media_ffprobe_json::json'
                               ' from mm_media where mm_media_guid'
                               ' in (select mm_media_guid from mm_media'
                               ' where mm_media_metadata_guid = $1'
                               ' offset $2 limit $3)',
                               guid, offset, records)


async def db_media_duplicate_detail_count(self, guid, db_connection=None):
    """
    # duplicate detail count
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_media'
                                  ' where mm_media_metadata_guid = $1',
                                  guid)


async def db_media_ffprobe_all_guid(self, media_uuid, media_class_uuid, db_connection=None):
    """
    # fetch all media with METADATA match
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # take off ::json due to distinct
    return await db_conn.fetch(
        'select distinct mm_media_guid,'
        ' mm_media_ffprobe_json'
        ' from mm_media, mm_metadata_movie'
        ' where mm_media_metadata_guid = '
        '(select mm_media_metadata_guid'
        ' from mm_media where mm_media_guid = $1)'
        ' and mm_media_class_guid = $2',
        media_uuid, media_class_uuid)


async def db_media_insert(self, media_uuid, media_path, media_class_uuid,
                          media_metadata_uuid, media_ffprobe_json, media_json, db_connection=None):
    """
    # insert media into database
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('insert into mm_media (mm_media_guid,'
                          ' mm_media_class_guid,'
                          ' mm_media_path,'
                          ' mm_media_metadata_guid,'
                          ' mm_media_ffprobe_json,'
                          ' mm_media_json)'
                          ' values ($1, $2, $3, $4, $5, $6)',
                          media_uuid, media_class_uuid, media_path,
                          media_metadata_uuid, media_ffprobe_json, media_json)


async def db_media_known(self, offset=0, records=None, db_connection=None):
    """
    # find all known media
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetch('select mm_media_path'
                               ' from mm_media where mm_media_guid'
                               ' in (select mm_media_guid'
                               ' from mm_media order by mm_media_path'
                               ' offset $1 limit $2) order by mm_media_path',
                               offset, records)


async def db_media_known_count(self, db_connection=None):
    """
    # count known media
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_media')


async def db_media_matched_count(self, db_connection=None):
    """
    # count matched media
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_media'
                                  ' where mm_media_metadata_guid is not NULL')


async def db_media_new(self, offset=None, records=None, search_value=None,
                       days_old=7, db_connection=None):
    """
    # new media
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if offset is None:
        return await db_conn.fetch('select mm_media_name,'
                                   ' mm_media_guid,'
                                   ' mm_media_class_guid'
                                   ' from mm_media, mm_metadata_movie'
                                   ' where mm_media_metadata_guid = mm_metadata_guid'
                                   ' and mm_media_json->>\'DateAdded\' >= $1'
                                   ' order by LOWER(mm_media_name),'
                                   ' mm_media_class_guid',
                                   (datetime.datetime.now()
                                    - datetime.timedelta(days=days_old)).strftime(
                                       "%Y-%m-%d"))
    else:
        return await db_conn.fetch('select mm_media_name,'
                                   ' mm_media_guid,'
                                   ' mm_media_class_guid'
                                   ' from mm_media, mm_metadata_movie'
                                   ' where mm_media_metadata_guid = mm_metadata_guid'
                                   ' and mm_media_json->>\'DateAdded\' >= $1'
                                   ' order by LOWER(mm_media_name),'
                                   ' mm_media_class_guid offset $2 limit $3',
                                   (datetime.datetime.now()
                                    - datetime.timedelta(days=days_old)).strftime(
                                       "%Y-%m-%d"),
                                   offset, records)


async def db_media_new_count(self, search_value=None, days_old=7, db_connection=None):
    """
    # new media count
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_media, mm_metadata_movie'
                                  ' where mm_media_metadata_guid = mm_metadata_guid'
                                  ' and mm_media_json->>\'DateAdded\' >= $1',
                                  (datetime.datetime.now()
                                   - datetime.timedelta(days=days_old)).strftime(
                                      "%Y-%m-%d"))


async def db_media_path_by_uuid(self, media_uuid, db_connection=None):
    """
    # find path for media by uuid
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select mm_media_path from mm_media'
                                  ' where mm_media_guid = $1',
                                  media_uuid)


async def db_media_rating_update(self, media_guid, user_id, status_text, db_connection=None):
    """
    # set favorite status for media
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if status_text == 'watched' or status_text == 'mismatch':
        status_setting = True
    else:
        status_setting = status_text
        status_text = 'Rating'
    try:
        json_data = await db_conn.fetchval('SELECT mm_media_json::json from mm_media'
                                           ' where mm_media_guid = $1 FOR UPDATE',
                                           media_guid)
        if 'UserStats' not in json_data:
            json_data['UserStats'] = {}
        if user_id in json_data['UserStats']:
            json_data['UserStats'][user_id][status_text] = status_setting
        else:
            json_data['UserStats'][user_id] = {status_text: status_setting}
        # since 'for update' must release record on fail
        self.db_update_media_json(media_guid, json.dumps(json_data))
        self.db_commit()
    except:
        self.db_rollback()
        return None


async def db_media_unmatched_list(self, offset=0, list_limit=None, db_connection=None):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetch('select mm_media_guid,'
                               ' mm_media_path from mm_media'
                               ' where mm_media_metadata_guid is NULL'
                               ' order by mm_media_path offset $1 limit $2',
                               offset, list_limit)


async def db_media_unmatched_list_count(self, db_connection=None):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_media'
                                  ' where mm_media_metadata_guid is NULL')


async def db_update_media_id(self, media_guid, metadata_guid, db_connection=None):
    """
    # update the mediaid
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('update mm_media set mm_media_metadata_guid = $1'
                          ' where mm_media_guid = $2', metadata_guid, media_guid)
