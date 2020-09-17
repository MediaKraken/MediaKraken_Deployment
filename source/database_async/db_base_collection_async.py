import json
import uuid


async def db_collection_list(self, offset=None, records=None, search_value=None,
                             db_connection=None):
    """
    Return collections list from the database
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if offset is None:
        if search_value is not None:
            return await self.db_connection.fetch('select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json::json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_name % $1'
                                                  ' order by mm_metadata_collection_name',
                                                  search_value)
        else:
            return await self.db_connection.fetch('select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json::json'
                                                  ' from mm_metadata_collection'
                                                  ' order by mm_metadata_collection_name')
    else:
        if search_value is not None:
            return await self.db_connection.fetch('select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json::json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_guid'
                                                  ' in (select mm_metadata_collection_guid'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_name % $1'
                                                  ' order by mm_metadata_collection_name'
                                                  ' offset $2 limit $3)'
                                                  ' order by mm_metadata_collection_name',
                                                  search_value, offset, records)
        else:
            return await self.db_connection.fetch('select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json::json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_guid'
                                                  ' in (select mm_metadata_collection_guid'
                                                  ' from mm_metadata_collection'
                                                  ' order by mm_metadata_collection_name'
                                                  ' offset $1 limit $2) '
                                                  'order by mm_metadata_collection_name',
                                                  offset, records)


async def db_collection_list_count(self, search_value=None, db_connection=None):
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_collection'
                                                 ' where mm_metadata_collection_name = $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_collection')


async def db_collection_read_by_guid(self, media_uuid, db_connection=None):
    """
    Collection details
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetchrow('select mm_metadata_collection_json,'
                                             ' mm_metadata_collection_imagelocal_json::json'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_guid = $1',
                                             media_uuid)


async def db_media_collection_scan(self, db_connection=None):
    """
    Returns a list of movies that belong in a collection specifified by tmdb
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetch('select mm_metadata_guid, mm_metadata_json'
                                          ' from mm_metadata_movie'
                                          ' where mm_metadata_json->\'belongs_to_collection\'::text'
                                          ' <> \'{}\'::text'
                                          ' order by mm_metadata_json->\'belongs_to_collection\'')


async def db_collection_guid_by_name(self, collection_name, db_connection=None):
    """
    Return uuid from collection name
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetchval(
        'select mm_metadata_collection_guid from mm_metadata_collection'
        ' where mm_metadata_collection_name->>\'name\' = $1',
        collection_name)


async def db_collection_by_tmdb(self, tmdb_id, db_connection=None):
    """
    Return uuid via tmdb id
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await self.db_connection.fetchval(
        'select mm_metadata_collection_guid from mm_metadata_collection'
        ' where mm_metadata_collection_json @> \'{"id":$1}\'', tmdb_id)


async def db_collection_insert(self, collection_name, guid_json, metadata_json,
                               localimage_json, db_connection=None):
    """
    Insert collection into the database
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute(
        'insert into mm_metadata_collection (mm_metadata_collection_guid,'
        ' mm_metadata_collection_name, mm_metadata_collection_media_ids,'
        ' mm_metadata_collection_json, mm_metadata_collection_imagelocal_json)'
        ' values ($1,$2,$3,$4,$5)', new_guid, json.dumps(collection_name),
        json.dumps(guid_json),
        json.dumps(metadata_json),
        json.dumps(localimage_json))
    return new_guid


async def db_collection_update(self, collection_guid, guid_json, db_connection=None):
    """
    Update the ids listed within a collection
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await self.db_connection.execute('update mm_metadata_collection'
                                     ' set mm_metadata_collection_media_ids = $1,'
                                     ' mm_metadata_collection_json = $2'
                                     ' where mm_metadata_collection_guid = $3',
                                     TODOfield, json.dumps(guid_json), collection_guid)
