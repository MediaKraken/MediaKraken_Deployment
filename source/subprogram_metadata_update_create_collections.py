
# pull in all metadata with part of collection in metadata
old_collection_name = ''
old_poster_path = None
old_backdrop_path = None
old_id = None
guid_list = []
first_record = True
total_collections_downloaded = 0
for row_data in db_connection.db_media_collection_scan():
    # mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids
    if old_collection_name != \
            row_data['mm_metadata_json']['belongs_to_collection']['name']:
        if not first_record:
            db_connection.db_download_insert(provider='themoviedb',
                                             down_json=json.dumps({'Status': 'FetchCollection',
                                                                   'Name': old_collection_name,
                                                                   'GUID': guid_list,
                                                                   'Poster': old_poster_path,
                                                                   'Backdrop': old_backdrop_path,
                                                                   'ProviderMetaID': old_id}))
            total_collections_downloaded += 1
        old_collection_name = \
            row_data['mm_metadata_json']['belongs_to_collection']['name']
        old_poster_path = \
            row_data['mm_metadata_json']['belongs_to_collection']['poster_path']
        old_backdrop_path = row_data['mm_metadata_json']['belongs_to_collection']['backdrop_path']
        old_id = \
            row_data['mm_metadata_json']['belongs_to_collection']['id']
        guid_list = []
        first_record = False
    guid_list.append(row_data['mm_metadata_guid'])
# do last insert/update
if len(guid_list) > 0:
    # TODO this will break with new download code
    db_connection.db_download_insert(provider='themoviedb',
                                     down_json=json.dumps({'Status': 'FetchCollection',
                                                           'Name': old_collection_name,
                                                           'GUID': guid_list,
                                                           'Poster': old_poster_path,
                                                           'Backdrop': old_backdrop_path,
                                                           'ProviderMetaID': old_id}))
    total_collections_downloaded += 1

