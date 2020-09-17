import datetime

from common import common_logging_elasticsearch_httpx


async def db_media_sports_list(self, class_guid, offset=None, list_limit=0,
                               search_text=None,
                               list_type=None, list_genre='All',
                               group_collection=False, include_remote=False, db_connection=None):
    """
    # sports media return
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "classuid": class_guid,
                                                                         'type': list_type,
                                                                         'genre':
                                                                             list_genre})
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "group and remote": group_collection,
                                                                         'remote': include_remote})
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "list, offset": list_limit,
                                                                         'offset': offset})
    # messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= '
                                                              '$2) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"))
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= '
                                                              '$2) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $3 '
                                                              'limit $4',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              offset, list_limit)
                else:
                    if offset is None:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid,'
                                                              ' mmr_media_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' NULL as '
                                                              'mmr_media_path'
                                                              ' from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $3 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid and '
                                                              'mmr_media_json->>\'DateAdded\' >= $4) '
                                                              'as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"))
                    else:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media,'
                                                              ' mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid,'
                                                              ' mmr_media_json::json, '
                                                              'mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $3 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid and '
                                                              'mmr_media_json->>\'DateAdded\' >= $4) '
                                                              'as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $5 '
                                                              'limit $6',
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
                    return await self.db_connection.fetch('select 1')
                else:
                    return await self.db_connection.fetch('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid)
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $2 '
                                                              'limit $3',
                                                              class_guid, offset, list_limit)
                else:
                    if offset is None:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid,'
                                                              ' mmr_media_json::json, '
                                                              'mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $2 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid)) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, class_guid)
                    else:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json::json,'
                                                              ' mm_metadata_sports_image_json::json,'
                                                              ' mm_media_path'
                                                              ' from mm_media,'
                                                              ' mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid, mmr_media_json::json, '
                                                              'mm_metadata_sports_image_json::json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $2 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid)) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $3 '
                                                              'limit $4',
                                                              class_guid, class_guid, offset,
                                                              list_limit)
            else:
                if not include_remote:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name as name,'
                                                              ' mm_media_guid as guid,'
                                                              ' mm_metadata_sports_user_json::json as mediajson,'
                                                              ' mm_metadata_sports_image_json::json as metajson,'
                                                              ' mm_media_path as mediapath from mm_media,'
                                                              ' mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and (mm_metadata_sports_json->>\'belongs_to_collection\') is null'
                                                              ' union select mm_metadata_collection_name as name,'
                                                              ' mm_metadata_collection_guid as guid, null::jsonb as metajson,'
                                                              ' mm_media_path as mediapath'
                                                              ' from mm_metadata_collection) as temp'
                                                              ' order by LOWER(name)',
                                                              class_guid)
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name as name,'
                                                              ' mm_media_guid as guid,'
                                                              ' mm_metadata_sports_user_json::json as mediajson,'
                                                              ' mm_metadata_sports_image_json::json as metajson,'
                                                              ' mm_media_path as mediapath'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and (mm_metadata_sports_json->>\'belongs_to_collection\') is null'
                                                              ' union select mm_metadata_collection_name as name,'
                                                              ' mm_metadata_collection_guid as guid, null::jsonb as metajson,'
                                                              ' mm_media_path as mediapath'
                                                              ' from mm_metadata_collection) as temp'
                                                              ' order by LOWER(name) offset $2 limit $3',
                                                              class_guid, offset, list_limit)
                else:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name as name,'
                                                              ' mm_media_guid as guid,'
                                                              ' mm_metadata_sports_user_json::json as mediajson,'
                                                              ' mm_metadata_sports_image_json::json as metaimagejson,'
                                                              ' mm_media_path as mediapath'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and (mm_metadata_sports_json->>\'belongs_to_collection\') is null'
                                                              # TODO put back in
                                                              #                        ' union select mm_metadata_collection_name as name,'
                                                              #                        ' mm_metadata_collection_guid as guid,'
                                                              #                        ' null::jsonb as mediajson, null::jsonb as metajson,'
                                                              #                        ' null::jsonb as metaimagejson, mm_media_path as mediapath'
                                                              #                        ' from mm_metadata_collection'
                                                              ') as temp'
                                                              ' order by LOWER(name)',
                                                              class_guid)
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name as name,'
                                                              ' mm_media_guid as guid,'
                                                              ' mm_metadata_sports_user_json as mediajson,'
                                                              ' mm_metadata_sports_image_json as metaimagejson,'
                                                              ' mm_media_path as mediapath'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and (mm_metadata_sports_json->>\'belongs_to_collection\') is null'
                                                              # TODO put back in
                                                              #                        ' union select mm_metadata_collection_name as name,'
                                                              #                        ' mm_metadata_collection_guid as guid,'
                                                              #                        ' null::jsonb as mediajson, null::jsonb as metajson,'
                                                              #                        ' null::jsonb as metaimagejson, mm_media_path as mediapath'
                                                              #                        ' from mm_metadata_collection'
                                                              ') as temp'
                                                              ' order by LOWER(name) offset $2 limit $3',
                                                              class_guid, offset, list_limit)
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              list_genre)
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $4 '
                                                              'limit $5',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              list_genre, offset, list_limit)
                else:
                    if offset is None:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid, mmr_media_json, '
                                                              'mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $4'
                                                              ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mmr_media_json->>\'DateAdded\' >= $5'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $6)) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              list_genre)
                    else:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_media_json->>\'DateAdded\' >= $2'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3)'
                                                              ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                                              ' mmr_media_guid,'
                                                              ' mmr_media_json, '
                                                              'mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $4'
                                                              ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mmr_media_json->>\'DateAdded\' >= $5'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $6)) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $7 '
                                                              'limit $8',
                                                              class_guid, (datetime.datetime.now()
                                                                           - datetime.timedelta(
                                        days=7)).strftime(
                                "%Y-%m-%d"),
                                                              list_genre, offset, list_limit)

            else:
                return await self.db_connection.fetch('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, list_genre)
                    else:
                        return await self.db_connection.fetch('select * from (select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $3 '
                                                              'limit $4',
                                                              class_guid, list_genre, offset,
                                                              list_limit)

                else:
                    if offset is None:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media,'
                                                              ' mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2)'
                                                              ' union (select distinct on (mmr_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mmr_media_guid,'
                                                              ' mmr_media_json,'
                                                              ' mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $3 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $4)) as temp'
                                                              ' order by LOWER(mm_metadata_sports_name)',
                                                              class_guid, list_genre, class_guid,
                                                              list_genre)
                    else:
                        return await self.db_connection.fetch('select * from ((select distinct'
                                                              ' on (mm_media_metadata_guid)'
                                                              ' mm_metadata_sports_name, mm_media_guid,'
                                                              ' mm_metadata_sports_user_json,'
                                                              ' mm_metadata_sports_image_json,'
                                                              ' mm_media_path'
                                                              ' from mm_media, mm_metadata_sports'
                                                              ' where mm_media_class_guid = $1'
                                                              ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                              ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2)'
                                                              ' union (select distinct on (mmr_media_metadata_guid)'
                                                              ' mm_metadata_sports_name,'
                                                              ' mmr_media_guid, mmr_media_json,'
                                                              ' mm_metadata_sports_image_json, NULL as '
                                                              'mmr_media_path'
                                                              '  from mm_media_remote, mm_metadata_sports'
                                                              ' where mmr_media_class_guid = $3 and '
                                                              'mmr_media_metadata_guid'
                                                              ' = mm_metadata_sports_guid and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $4)) as temp'
                                                              ' order by LOWER('
                                                              'mm_metadata_sports_name) offset $5 '
                                                              'limit $6',
                                                              class_guid, list_genre, class_guid,
                                                              list_genre,
                                                              offset, list_limit)
            else:
                if offset is None:
                    return await self.db_connection.fetch('select 1')
                else:
                    return await self.db_connection.fetch('select 1')


async def db_media_sports_list_count(self, class_guid, list_type=None,
                                     list_genre='All',
                                     group_collection=False, include_remote=False,
                                     search_text=None, db_connection=None):
    """
    # sports media count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "classuid counter":
                                                                             class_guid,
                                                                         'type': list_type,
                                                                         'genre': list_genre})
    # messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    return await self.db_connection.fetchval('select count(*) from (select distinct'
                                                             ' mm_metadata_sports_guid'
                                                             ' from mm_media,'
                                                             ' mm_metadata_sports'
                                                             ' where mm_media_class_guid = $1'
                                                             ' and mm_media_metadata_guid'
                                                             ' = mm_metadata_sports_guid'
                                                             ' and mm_media_json->>\'DateAdded\' >= $2)'
                                                             ' as temp',
                                                             class_guid, (datetime.datetime.now()
                                                                          - datetime.timedelta(
                                    days=7)).strftime("%Y-%m-%d"))
                else:
                    return await self.db_connection.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_sports_guid from mm_media,'
                        ' mm_metadata_sports'
                        ' where mm_media_class_guid = $1'
                        ' and mm_media_metadata_guid'
                        ' = mm_metadata_sports_guid'
                        ' and mm_media_json->>\'DateAdded\' >= $2)'
                        ' union (select distinct mmr_metadata_guid'
                        ' from mm_media_remote,'
                        ' mm_metadata_sports where '
                        'mmr_media_class_guid = $3'
                        ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                        ' and mm_media_json->>\'DateAdded\' >= '
                        '$4)) as temp',
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"),
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"))
            else:
                return await self.db_connection.fetchval('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    return await self.db_connection.fetchval('select count(*) from (select distinct'
                                                             ' mm_metadata_sports_guid'
                                                             ' from mm_media,'
                                                             ' mm_metadata_sports'
                                                             ' where mm_media_class_guid = $1'
                                                             ' and mm_media_metadata_guid'
                                                             ' = mm_metadata_sports_guid) as temp',
                                                             class_guid)
                else:
                    return await self.db_connection.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_sports_guid'
                        ' from mm_media, mm_metadata_sports'
                        ' where mm_media_class_guid = $1 and '
                        'mm_media_metadata_guid'
                        ' = mm_metadata_sports_guid)'
                        ' union (select distinct mm_metadata_sports_guid'
                        ' from mm_media_remote, mm_metadata_sports'
                        ' where mmr_media_class_guid = $2'
                        ' and mmr_media_metadata_guid = mm_metadata_sports_guid)) as temp',
                        class_guid, class_guid)
            else:
                if not include_remote:
                    return await self.db_connection.fetchval('select count(*) as row_count'
                                                             ' from ((select distinct mm_metadata_sports_guid from mm_media,'
                                                             ' mm_metadata_sports'
                                                             ' where mm_media_class_guid = $1'
                                                             ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                                             ' and (mm_metadata_sports_json->>\'belongs_to_collection\') is null)'
                                                             ' union (select count(*) from xxxx as row_count)) as temp',
                                                             class_guid, class_guid)
                else:
                    return await self.db_connection.fetchval('select 1')
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    return await self.db_connection.fetchval('select count(*) from (select distinct'
                                                             ' mm_metadata_sports_guid'
                                                             ' from mm_media, mm_metadata_sports'
                                                             ' where mm_media_class_guid = $1 and '
                                                             'mm_media_metadata_guid'
                                                             ' = mm_metadata_sports_guid and '
                                                             'mm_media_json->>\'DateAdded\' >= $2'
                                                             ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3) as temp',
                                                             class_guid, (datetime.datetime.now()
                                                                          - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre)
                else:
                    return await self.db_connection.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_sports_guid'
                        ' from mm_media, mm_metadata_sports'
                        ' where mm_media_class_guid = $1 and '
                        'mm_media_metadata_guid'
                        ' = mm_metadata_sports_guid and '
                        'mm_media_json->>\'DateAdded\' >= $2'
                        ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $3)'
                        ' union (select distinct mmr_metadata_guid from mm_media_remote,'
                        ' mm_metadata_sports'
                        ' where mmr_media_class_guid = $4'
                        ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                        ' and mmr_media_json->>\'DateAdded\' >= $5'
                        ' and '
                        'mm_metadata_sports_json->\'genres\'->0->\'name\' ? $6)) as temp',
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre,
                        class_guid, (datetime.datetime.now()
                                     - datetime.timedelta(
                                    days=7)).strftime(
                            "%Y-%m-%d"), list_genre)
            else:
                return await self.db_connection.fetchval('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    return await self.db_connection.fetchval('select count(*) from (select distinct'
                                                             ' mm_metadata_sports_guid'
                                                             ' from mm_media, mm_metadata_sports'
                                                             ' where mm_media_class_guid = $1 and '
                                                             'mm_media_metadata_guid'
                                                             ' = mm_metadata_sports_guid and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2)'
                                                             ' as temp', class_guid, list_genre)
                else:
                    return await self.db_connection.fetchval(
                        'select count(*) from ((select distinct'
                        ' mm_metadata_sports_guid'
                        ' from mm_media, mm_metadata_sports'
                        ' where mm_media_class_guid = $1 and'
                        ' mm_media_metadata_guid'
                        ' = mm_metadata_sports_guid'
                        ' and mm_metadata_sports_json->\'genres\'->0->\'name\' ? $2)'
                        ' union (select distinct mmr_media_metadata_guid'
                        ' from mm_media_remote,'
                        ' mm_metadata_sports'
                        ' where mmr_media_class_guid = $3'
                        ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                        ' and'
                        ' mm_metadata_sports_json->\'genres\'->0->\'name\' ? $4)) as temp',
                        class_guid, list_genre, class_guid,
                        list_genre)
            else:
                return await self.db_connection.fetchval('select 1')
