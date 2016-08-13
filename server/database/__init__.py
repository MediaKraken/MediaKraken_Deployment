class MK_Server_Database(object):
    from db_base import srv_db_Open,\
        srv_db_Open_Isolation,\
        srv_db_Close,\
        srv_db_Commit,\
        srv_db_Rollback,\
        srv_db_table_index_check,\
        srv_db_Table_Count,\
        srv_db_Query
    from db_base_activity import srv_db_Activity_Insert,\
        srv_db_Activity_Purge
    from db_base_audit import srv_db_Audit_Path_Status,\
        srv_db_Audit_Path_Update_Status,\
        srv_db_Audit_Paths_Count,\
        srv_db_Audit_Path_Update_By_UUID,\
        srv_db_Audit_Path_Add,\
        srv_db_Audit_Path_Check,\
        srv_db_Audit_Directory_Timestamp_Update,\
        srv_db_Audit_Paths,\
        srv_db_Audit_Path_Delete,\
        srv_db_Audit_Path_By_UUID
    from db_base_channel import srv_db_Channel_Insert
    from db_base_collection import srv_db_media_collection_scan,\
        srv_db_collection_guid_by_name,\
        srv_db_collection_insert,\
        srv_db_collection_update,\
        srv_db_collection_list,\
        srv_db_collection_read_by_guid,\
        srv_db_collection_by_tmdb
    from db_base_cron import srv_db_Cron_List_Count,\
        srv_db_Cron_List,\
        srv_db_Cron_Time_Update
    from db_base_device import srv_db_Device_Count,\
        srv_db_Device_List,\
        srv_db_Device_Insert,\
        srv_db_Device_Update,\
        srv_db_Device_Delete,\
        srv_db_Device_Read
    from db_base_download import srv_db_Download_Insert,\
        srv_db_Download_Read_By_Provider,\
        srv_db_Download_Delete,\
        srv_db_Download_Update_Provider,\
        srv_db_Download_Update
    from db_base_kodi import srv_db_Kodi_User_Sync,\
        srv_db_Kodi_User_Sync_List_Added
    from db_base_iradio import srv_db_iRadio_Insert,\
        srv_db_iRadio_List_Count,\
        srv_db_iRadio_List
    from db_base_link import srv_db_Link_List_Count,\
        srv_db_Link_List,\
        srv_db_Link_Insert,\
        srv_db_Link_Delete
    from db_base_media_class import srv_db_media_class_list_count,\
        srv_db_media_class_list,\
        srv_db_media_class_by_uuid,\
        srv_db_media_uuid_by_class
    from db_base_media_games from common import common_Media_Game_System_List_Count,\
        com_media_game_system_list,\
        com_media_game_list_by_system_count,\
        com_media_game_list_by_system,\
        com_media_game_list_count,\
        com_media_game_list
    from db_base_media_images from common import common_Media_Images_List_Count,\
        com_media_images_list
    from db_base_media import srv_db_insert_media,\
        srv_db_read_media,\
        srv_db_known_media_count,\
        srv_db_known_media,\
        srv_db_matched_media_count,\
        srv_db_known_media_All_Unmatched_Count,\
        srv_db_known_media_All_Unmatched,\
        srv_db_media_duplicate_count,\
        srv_db_media_duplicate,\
        srv_db_media_duplicate_Detail_Count,\
        srv_db_media_duplicate_Detail,\
        srv_db_media_path_by_uuid,\
        srv_db_media_watched_status_update,\
        srv_db_update_media_id,\
        srv_db_update_media_json,\
        srv_db_known_media_Chapter_Scan,\
        srv_db_media_by_metadata_guid,\
        srv_db_media_image_path,\
        srv_db_read_media_Metadata_Both,\
        srv_db_read_media_Path_Like,\
        srv_db_read_media_New,\
        srv_db_read_media_New_Count,\
        srv_db_media_watched_checkpoint_update,\
        srv_db_media_favorite_status_update,\
        srv_db_media_poo_status_update,\
        srv_db_media_mismatch_status_update
    from db_base_media_movie import srv_db_web_media_list_count,\
        srv_db_media_movie_count_by_genre,\
        srv_db_web_media_list,\
        srv_db_media_random
    from db_base_media_music import srv_db_media_album_count,\
        srv_db_media_album_list
    from db_base_media_remote import srv_db_insert_remote_media,\
        srv_db_read_remote_media,\
        srv_db_known_remote_media_count,\
        srv_db_media_remote_read_new
    from db_base_media_tv import srv_db_web_tvmedia_list,\
        srv_db_web_tvmedia_list_Count
    from db_base_metadata import srv_db_read_media_Metadata,\
        srv_db_metadata_genre_list_count,\
        srv_db_metadata_genre_list,\
        srv_db_metadata_movie_count_by_genre,\
        srv_db_Metadata_GUID_By_imdb,\
        srv_db_metadata_guid_by_tvdb,\
        srv_db_metadata_guid_by_tmdb,\
        srv_db_metadata_guid_by_rt,\
        srv_db_metadata_insert_tmdb,\
        srv_db_metadata_tmdb_count,\
        srv_db_metadata_movie_list,\
        srv_db_metadata_fetch_media_id_json,\
        srv_db_metadata_fetch_series_media_id_json,\
        srv_db_find_metadata_guid,\
        srv_db_metadata_update_Media_ID_From_Scudlee
    from db_base_metadata_book import srv_db_metadatabook_guid_by_isbn,\
        srv_db_metadatabook_guid_by_name,\
        srv_db_metadatabook_book_insert
    from db_base_metadata_games import srv_db_metadata_game_system_by_guid,\
        srv_db_metadata_game_system_list_count,\
        srv_db_metadata_game_system_list,\
        srv_db_metadata_game_list_count,\
        srv_db_metadata_game_list,\
        srv_db_metadata_game_by_guid
    from db_base_metadata_gamesdb import srv_db_metadata_gamesdb_system_insert
    from db_base_metadata_movie import srv_db_metadata_movie_update_castcrew
    from db_base_metadata_music import srv_db_music_lookup,\
        srv_db_metadata_musician_by_guid,\
        srv_db_metadata_musician_add,\
        srv_db_metadata_album_by_guid,\
        srv_db_metadata_album_add,\
        srv_db_metadata_song_by_guid,\
        srv_db_metadata_song_add,\
        srv_db_metadata_songs_by_album_guid,\
        srv_db_metadata_album_list,\
        srv_db_metadata_muscian_list
    from db_base_metadata_music_video import srv_db_metadata_music_video_lookup,\
        srv_db_metadata_music_video_add,\
        srv_db_metadata_music_video_detail_by_uuid,\
        srv_db_metadata_music_video_count,\
        srv_db_metadata_music_video_list
    from db_base_nas import srv_db_NAS_Count,\
        srv_db_NAS_List,\
        srv_db_NAS_Insert,\
        srv_db_NAS_Update,\
        srv_db_NAS_Delete,\
        srv_db_NAS_Read
    from db_base_metadata_people import srv_db_metadata_person_list_count,\
        srv_db_metadata_person_list,\
        srv_db_metadata_person_by_guid,\
        srv_db_metadata_person_by_name,\
        srv_db_metadata_person_insert_cast_crew,\
        srv_db_metdata_person_insert,\
        srv_db_metadata_person_id_count,\
        srv_db_metadata_person_as_seen_in
    from db_base_metadata_sports import srv_db_Metadata_Sports_GUID_By_thesportsdb,\
        srv_db_metadata_sports_list_count,\
        srv_db_metadata_sports_list,\
        srv_db_metadata_sports_guid_by_event_name
    from db_base_metadata_thesportsdb import srv_db_Metadatathesportsdb_Insert,\
        srv_db_metadatathesports_update,\
        srv_db_Metadatathesportsdb_Select_By_Guid
    from db_base_metadata_thetvdb import srv_db_metadatatvdb_insert,\
        srv_db_metadatatvdb_update
    from db_base_metadata_tv import srv_db_MetadataTV_GUID_By_imdb,\
        srv_db_metadatatv_guid_by_tvdb,\
        srv_db_MetadataTV_GUID_By_tvmaze,\
        srv_db_metadata_tvshow_list_count,\
        srv_db_metadata_tvshow_list,\
        srv_db_metadata_tvshow_detail,\
        srv_db_read_tvmetadata_episodes,\
        srv_db_metadatatv_guid_by_tvshow_name,\
        srv_db_metadata_tvshow_update_image,\
        srv_db_metadata_tvshow_images_to_update,\
        srv_db_read_tvmetadata_eps_season,\
        srv_db_read_tvmetadata_season_eps_list,\
        srv_db_read_tvmetadata_episode
    from db_base_metadata_tvmaze import srv_db_Metadatatvmaze_Changed_UUID,\
        srv_db_Metadatatvmaze_Insert,\
        srv_db_Metadatatvmaze_Update
    from db_base_notification import srv_db_Notification_Insert,\
        srv_db_Notification_Read
    from db_base_option_status import srv_db_Option_Status_Read,\
        srv_db_Option_Status_Update,\
        srv_db_Option_Status_Update_Scan_Json,\
        srv_db_Option_Status_Update_Scan_Json_Rec
    from db_base_postgresql import srv_db_Postgresql_Table_Sizes,\
        srv_db_Postgresql_Row_Count,\
        srv_db_Postgresql_Vacuum_Stat_By_Day,\
        srv_db_Postgresql_Vacuum_Table
    from db_base_review import srv_db_Review_Count,\
        srv_db_Review_List_By_TMDB_GUID,\
        srv_db_review_insert
    from db_base_sync import srv_db_Sync_List_Count,\
        srv_db_Sync_List,\
        srv_db_Sync_Insert,\
        srv_db_Sync_Delete,\
        srv_db_Sync_Progress_Update
    from db_base_triggers import srv_db_trigger_insert,\
        srv_db_triggers_read,\
        srv_db_triggers_delete
    from db_base_tuner import srv_db_tuner_count,\
        srv_db_tuner_insert,\
        srv_db_tuner_delete,\
        srv_db_tuner_list,\
        srv_db_tuner_by_serial,\
        srv_db_tuner_update
    from db_base_tv_schedule import srv_db_tv_stations_read,\
        srv_db_tv_stations_read_StationID_List,\
        srv_db_tv_station_insert,\
        srv_db_tv_station_exist,\
        srv_db_tv_station_update,\
        srv_db_tv_schedule_insert,\
        srv_db_tv_program_insert,\
        srv_db_tv_schedule_by_date
    from db_base_usage import srv_db_Usage_Top10_AllTime,\
        srv_db_Usage_Top10_Movie,\
        srv_db_Usage_Top10_TV_Show,\
        srv_db_Usage_Top10_TV_Episode
    from db_base_users import srv_db_User_List_Name_Count,\
        srv_db_User_List_Name,\
        srv_db_User_Detail,\
        srv_db_User_Delete,\
        srv_db_User_Login_Kodi

    # class variables
    sql3_conn = None
    sql3_cursor = None
