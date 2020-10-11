import datetime
import inspect

from common import common_logging_elasticsearch_httpx


#####################################
# Not using :;json due to unions
#####################################

async def db_media_movie_list(self, class_guid, list_type=None, list_genre='all',
                              list_limit=0, group_collection=False, offset=None,
                              include_remote=False,
                              search_text=None, db_connection=None):
    """
    # web media return
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
    if list_genre == 'all':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\''
                                                   ' asc',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"))
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path, mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $3 limit $4',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   offset, list_limit)
                else:
                    if offset is None:
                        return await db_conn.fetch('select mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path, mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid, mmr_media_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path, mm_metadata_json'
                                                   ' from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $3'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid and mmr_media_json->>\'DateAdded\' >= $4) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"))
                    else:
                        return await db_conn.fetch('mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path, mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid, mmr_media_json, '
                                                   'mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path,'
                                                   ' mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $3'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid and mmr_media_json->>\'DateAdded\' >= $4) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $5 limit $6',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   offset, list_limit)
            else:
                if offset is None:
                    return await db_conn.fetch('select 1')
                else:
                    return await db_conn.fetch('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid)
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   ' offset $2 limit $3',
                                                   class_guid, offset, list_limit)
                else:
                    if offset is None:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid,'
                                                   ' mmr_media_json, '
                                                   'mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path, mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $2'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, class_guid)
                    else:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid, mmr_media_json, '
                                                   'mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path, mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $2'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $3 limit $4',
                                                   class_guid, class_guid, offset,
                                                   list_limit)
            else:
                if not include_remote:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name as name,'
                                                   ' mm_media_guid as guid,'
                                                   ' mm_metadata_user_json as mediajson,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path as mediapath'
                                                   ' from mm_media, mm_metadata_movie,'
                                                   ' mm_metadata_json'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                                   ' union select mm_metadata_collection_name as name,'
                                                   ' mm_metadata_collection_guid as guid,'
                                                   ' nullb as metajson,'
                                                   ' mm_media_path as mediapath'
                                                   ' from mm_metadata_collection) as temp'
                                                   ' order by LOWER(name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid)
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name as name,'
                                                   ' mm_media_guid as guid,'
                                                   ' mm_metadata_user_json as mediajson,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path as mediapath,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media,'
                                                   ' mm_metadata_movie where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                                   ' union select mm_metadata_collection_name as name,'
                                                   ' mm_metadata_collection_guid as guid,'
                                                   ' nullb as metajson,'
                                                   ' mm_media_path as mediapath,'
                                                   ' mm_metadata_json'
                                                   ' from mm_metadata_collection) as temp'
                                                   ' order by LOWER(name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $2 limit $3',
                                                   class_guid, offset, list_limit)
                else:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name as name,'
                                                   ' mm_media_guid as guid,'
                                                   ' mm_metadata_user_json as mediajson,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path as mediapath,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                                   # TODO put back in
                                                   #                        ' union select mm_metadata_collection_name as name,'
                                                   #                        ' mm_metadata_collection_guid as guid,'
                                                   #                        ' nullb as mediajson, nullb as metajson,'
                                                   #                        ' nullb as metaimagejson, mm_media_path as mediapath'
                                                   #                        ' from mm_metadata_collection'
                                                   ') as temp'
                                                   ' order by LOWER(name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid)
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name as name,'
                                                   ' mm_media_guid as guid,'
                                                   ' mm_metadata_user_json as mediajson,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path as mediapath,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                                   # TODO put back in
                                                   #                        ' union select mm_metadata_collection_name as name,'
                                                   #                        ' mm_metadata_collection_guid as guid,'
                                                   #                        ' nullb as mediajson, nullb as metajson,'
                                                   #                        ' nullb as metaimagejson, mm_media_path as mediapath'
                                                   #                        ' from mm_metadata_collection'
                                                   ') as temp'
                                                   ' order by LOWER(name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $2 limit $3',
                                                   class_guid, offset, list_limit)
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   list_genre)
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $4 limit $5',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   list_genre, offset, list_limit)
                else:
                    if offset is None:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid,'
                                                   ' mmr_media_json, '
                                                   'mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path, mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $4'
                                                   ' and mmr_media_metadata_guid = mm_metadata_guid'
                                                   ' and mmr_media_json->>\'DateAdded\' >= $5'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? %6)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   list_genre, class_guid,
                                                   (datetime.datetime.now()
                                                    - datetime.timedelta(
                                                               days=7)).strftime(
                                                       "%Y-%m-%d"),
                                                   list_genre)
                    else:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_media_json->>\'DateAdded\' >= $2'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3)'
                                                   ' union (select distinct on (mmr_media_metadata_guid) mm_media_name,'
                                                   ' mmr_media_guid,'
                                                   ' mmr_media_json, '
                                                   'mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path,'
                                                   ' mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $4'
                                                   ' and mmr_media_metadata_guid = mm_metadata_guid'
                                                   ' and mmr_media_json->>\'DateAdded\' >= $5'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $6)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $7 limit $8',
                                                   class_guid, (datetime.datetime.now()
                                                                - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                   list_genre, class_guid,
                                                   (datetime.datetime.now()
                                                    - datetime.timedelta(
                                                               days=7)).strftime(
                                                       "%Y-%m-%d"),
                                                   list_genre, offset, list_limit)

            else:
                return await db_conn.fetch('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $2) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, list_genre)
                    else:
                        return await db_conn.fetch('select * from (select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path, mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $2) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $3 limit $4',
                                                   class_guid, list_genre, offset,
                                                   list_limit)

                else:
                    if offset is None:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid)'
                                                   ' mm_media_name, mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media, mm_metadata_movie'
                                                   ' where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $2)'
                                                   ' union (select distinct on (mmr_media_metadata_guid)'
                                                   ' mm_media_name,'
                                                   ' mmr_media_guid,'
                                                   ' mmr_media_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster, NULL as '
                                                   'mmr_media_path,'
                                                   ' mm_metadata_json'
                                                   '  from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $3'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? $4)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc',
                                                   class_guid, list_genre, class_guid,
                                                   list_genre)
                    else:
                        return await db_conn.fetch('select * from ((select distinct'
                                                   ' on (mm_media_metadata_guid) mm_media_name,'
                                                   ' mm_media_guid,'
                                                   ' mm_metadata_user_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' mm_media_path, mm_metadata_json'
                                                   ' from mm_media,'
                                                   ' mm_metadata_movie where mm_media_class_guid = $1'
                                                   ' and mm_media_metadata_guid = mm_metadata_guid'
                                                   ' and mm_metadata_json->\'genres\'->0->\'name\' ? $2)'
                                                   ' union (select distinct on (mmr_media_metadata_guid)'
                                                   ' mm_media_name,'
                                                   ' mmr_media_guid,'
                                                   ' mmr_media_json,'
                                                   ' mm_metadata_localimage_json->\'Poster\''
                                                   ' as mm_poster,'
                                                   ' NULL as mmr_media_path,'
                                                   ' mm_metadata_json'
                                                   ' from mm_media_remote, mm_metadata_movie'
                                                   ' where mmr_media_class_guid = $3'
                                                   ' and mmr_media_metadata_guid'
                                                   ' = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? $4)) as temp'
                                                   ' order by LOWER(mm_media_name),'
                                                   ' mm_metadata_json->>\'release_date\' asc'
                                                   ' offset $5 limit $6',
                                                   class_guid, list_genre, class_guid,
                                                   list_genre,
                                                   offset, list_limit)
            else:
                if offset is None:
                    return await db_conn.fetch('select 1')
                else:
                    return await db_conn.fetch('select 1')


async def db_media_movie_list_count(self, class_guid, list_type=None,
                                    list_genre='all',
                                    group_collection=False, include_remote=False, search_text=None,
                                    db_connection=None):
    """
    # web media count
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
    # messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'all':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    return await db_conn.fetchval('select count(*) from (select distinct'
                                                  ' mm_metadata_guid'
                                                  ' from mm_media, mm_metadata_movie'
                                                  ' where mm_media_class_guid = $1'
                                                  ' and mm_media_metadata_guid'
                                                  ' = mm_metadata_guid'
                                                  ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                  ' as temp',
                                                  class_guid, (datetime.datetime.now()
                                                               - datetime.timedelta(
                                    days=7)).strftime("%Y-%m-%d"), )
                else:
                    return await db_conn.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_guid from mm_media, mm_metadata_movie'
                        ' where mm_media_class_guid = $1'
                        ' and mm_media_metadata_guid'
                        ' = mm_metadata_guid'
                        ' and mm_media_json->>\'DateAdded\' >= $2)'
                        ' union (select distinct mmr_metadata_guid'
                        ' from mm_media_remote,'
                        ' mm_metadata_movie where mmr_media_class_guid = $3'
                        ' and mmr_media_metadata_guid = mm_metadata_guid'
                        ' and mm_media_json->>\'DateAdded\' >= $4)) as temp',
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"),
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"))
            else:
                return await db_conn.fetchval('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    return await db_conn.fetchval('select count(*) from (select distinct'
                                                  ' mm_metadata_guid'
                                                  ' from mm_media, mm_metadata_movie'
                                                  ' where mm_media_class_guid = $1'
                                                  ' and mm_media_metadata_guid'
                                                  ' = mm_metadata_guid) as temp',
                                                  class_guid)
                else:
                    return await db_conn.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_guid from mm_media, mm_metadata_movie'
                        ' where mm_media_class_guid = $1 and mm_media_metadata_guid'
                        ' = mm_metadata_guid)'
                        ' union (select distinct mm_metadata_guid'
                        ' from mm_media_remote, mm_metadata_movie'
                        ' where mmr_media_class_guid = $2'
                        ' and mmr_media_metadata_guid = mm_metadata_guid)) as temp',
                        class_guid, class_guid)
            else:
                if not include_remote:
                    return await db_conn.fetchval('select count(*) as row_count'
                                                  ' from ((select distinct mm_metadata_guid from mm_media,'
                                                  ' mm_metadata_movie where mm_media_class_guid = $1'
                                                  ' and mm_media_metadata_guid = mm_metadata_guid'
                                                  ' and (mm_metadata_json->>\'belongs_to_collection\') is null)'
                                                  ' union (select count(*) from xxxx as row_count)) as temp',
                                                  class_guid, class_guid)
                else:
                    return await db_conn.fetchval('select 1')
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    return await db_conn.fetchval('select count(*) from (select distinct'
                                                  ' mm_metadata_guid from mm_media,'
                                                  ' mm_metadata_movie'
                                                  ' where mm_media_class_guid = $1'
                                                  ' and mm_media_metadata_guid'
                                                  ' = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= $2'
                                                  ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3) as temp',
                                                  class_guid, (datetime.datetime.now()
                                                               - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre)
                else:
                    return await db_conn.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_guid from mm_media, mm_metadata_movie'
                        ' where mm_media_class_guid = $1 and mm_media_metadata_guid'
                        ' = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= $2'
                        ' and mm_metadata_json->\'genres\'->0->\'name\' ? $3)'
                        ' union (select distinct mmr_metadata_guid from mm_media_remote,'
                        ' mm_metadata_movie where mmr_media_class_guid = $4'
                        ' and mmr_media_metadata_guid = mm_metadata_guid'
                        ' and mmr_media_json->>\'DateAdded\' >= $5'
                        ' and mm_metadata_json->\'genres\'->0->\'name\' ? $6)) as temp',
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre,
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre)
            else:
                return await db_conn.fetchval('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    return await db_conn.fetchval('select count(*) from (select distinct'
                                                  ' mm_metadata_guid from mm_media,'
                                                  ' mm_metadata_movie'
                                                  ' where mm_media_class_guid = $1 '
                                                  'and mm_media_metadata_guid'
                                                  ' = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? $2)'
                                                  ' as temp', class_guid, list_genre)
                else:
                    return await db_conn.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_guid'
                        ' from mm_media, mm_metadata_movie'
                        ' where mm_media_class_guid = $1 and mm_media_metadata_guid'
                        ' = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? $2)'
                        ' union (select distinct mmr_media_metadata_guid from mm_media_remote,'
                        ' mm_metadata_movie where mmr_media_class_guid = $3'
                        ' and mmr_media_metadata_guid = mm_metadata_guid'
                        ' and mm_metadata_json->\'genres\'->0->\'name\' ? $4)) as temp',
                        class_guid, list_genre, class_guid,
                        list_genre)
            else:
                return await db_conn.fetchval('select 1')


async def db_media_movie_count_by_genre(self, class_guid, db_connection=None):
    """
    # movie count by genre
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
    return await db_conn.fetch(
        'select mm_metadata_json->\'genres\' as gen,'
        ' count(mm_metadata_json->\'genres\') as gen_count'
        ' from ((select distinct on (mm_media_metadata_guid)'
        ' mm_metadata_json from mm_media, mm_metadata_movie'
        ' where mm_media_class_guid = $1'
        ' and mm_media_metadata_guid = mm_metadata_guid) union (select distinct'
        ' on (mmr_media_metadata_guid) mm_metadata_json from mm_media_remote,'
        ' mm_metadata_movie where mmr_media_class_guid = $2'
        ' and mmr_media_metadata_guid = mm_metadata_guid))'
        ' as temp group by gen',
        class_guid, class_guid)
