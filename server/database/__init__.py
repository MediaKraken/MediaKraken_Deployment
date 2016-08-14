class MKServerDatabase(object):
    """
    Main database class for server
    """
    from db_base import srv_db_open,\
        srv_db_open_isolation,\
        srv_db_close,\
        srv_db_commit,\
        srv_db_rollback,\
        srv_db_table_index_check,\
        srv_db_table_count,\
        srv_db_query
    from db_base_activity import srv_db_activity_insert,\
        srv_db_activity_purge
    from db_base_audit import srv_db_audit_path_status,\
        srv_db_audit_path_update_status,\
        srv_db_audit_paths_count,\
        srv_db_audit_path_update_by_uuid,\
        srv_db_audit_path_add,\
        srv_db_audit_path_check,\
        srv_db_audit_directory_timestamp_update,\
        srv_db_audit_paths,\
        srv_db_audit_path_delete,\
        srv_db_audit_path_by_uuid
    from db_base_channel import srv_db_channel_insert
    from db_base_collection import srv_db_media_collection_scan,\
        srv_db_collection_guid_by_name,\
        srv_db_collection_insert,\
        srv_db_collection_update,\
        srv_db_collection_list,\
        srv_db_collection_read_by_guid,\
        srv_db_collection_by_tmdb
    from db_base_cron import srv_db_cron_list_count,\
        srv_db_cron_list,\
        srv_db_cron_time_update
    from db_base_device import srv_db_device_count,\
        srv_db_device_list,\
        srv_db_device_insert,\
        srv_db_device_update,\
        srv_db_device_delete,\
        srv_db_device_read
    from db_base_download import srv_db_download_insert,\
        srv_db_download_read_by_provider,\
        srv_db_download_delete,\
        srv_db_download_update_provider,\
        srv_db_download_update
    from db_base_kodi import srv_db_kodi_user_sync,\
        srv_db_kodi_user_sync_list_added
    from db_base_iradio import srv_db_iradio_insert,\
        srv_db_iradio_list_count,\
        srv_db_iradio_list
    from db_base_link import srv_db_link_list_count,\
        srv_db_link_list,\
        srv_db_link_insert,\
        srv_db_link_delete
    from db_base_media_class import srv_db_media_class_list_count,\
        srv_db_media_class_list,\
        srv_db_media_class_by_uuid,\
        srv_db_media_uuid_by_class
    from db_base_media_games import srv_db_media_game_system_list_count,\
        srv_db_media_game_system_list,\
        srv_db_media_game_list_by_system_count,\
        srv_db_media_game_list_by_system,\
        srv_db_media_game_list_count,\
        srv_db_media_game_list
    from db_base_media_images import srv_db_media_images_list_count,\
        srv_db_media_images_list
    from db_base_media import srv_db_insert_media,\
        srv_db_read_media,\
        srv_db_known_media_count,\
        srv_db_known_media,\
        srv_db_matched_media_count,\
        srv_db_known_media_all_unmatched_count,\
        srv_db_known_media_all_unmatched,\
        srv_db_media_duplicate_count,\
        srv_db_media_duplicate,\
        srv_db_media_duplicate_detail_count,\
        srv_db_media_duplicate_detail,\
        srv_db_media_path_by_uuid,\
        srv_db_media_watched_status_update,\
        srv_db_update_media_id,\
        srv_db_update_media_json,\
        srv_db_known_media_chapter_scan,\
        srv_db_media_by_metadata_guid,\
        srv_db_media_image_path,\
        srv_db_read_media_metadata_both,\
        srv_db_read_media_path_like,\
        srv_db_read_media_new,\
        srv_db_read_media_new_count,\
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
        srv_db_web_tvmedia_list_count
    from db_base_metadata import srv_db_read_media_metadata,\
        srv_db_meta_genre_list_count,\
        srv_db_meta_genre_list,\
        srv_db_meta_movie_count_by_genre,\
        srv_db_meta_guid_by_imdb,\
        srv_db_meta_guid_by_tvdb,\
        srv_db_meta_guid_by_tmdb,\
        srv_db_meta_guid_by_rt,\
        srv_db_meta_insert_tmdb,\
        srv_db_meta_tmdb_count,\
        srv_db_meta_movie_list,\
        srv_db_meta_fetch_media_id_json,\
        srv_db_meta_fetch_series_media_id_json,\
        srv_db_find_metadata_guid,\
        srv_db_meta_update_media_id_from_scudlee
    from db_base_metadata_book import srv_db_metabook_guid_by_isbn,\
        srv_db_metabook_guid_by_name,\
        srv_db_metabook_book_insert
    from db_base_metadata_games import srv_db_meta_game_system_by_guid,\
        srv_db_meta_game_system_list_count,\
        srv_db_meta_game_system_list,\
        srv_db_meta_game_list_count,\
        srv_db_meta_game_list,\
        srv_db_meta_game_by_guid
    from db_base_metadata_gamesdb import srv_db_meta_gamesdb_system_insert
    from db_base_metadata_movie import srv_db_meta_movie_update_castcrew
    from db_base_metadata_music import srv_db_music_lookup,\
        srv_db_meta_musician_by_guid,\
        srv_db_meta_musician_add,\
        srv_db_meta_album_by_guid,\
        srv_db_meta_album_add,\
        srv_db_meta_song_by_guid,\
        srv_db_meta_song_add,\
        srv_db_meta_songs_by_album_guid,\
        srv_db_meta_album_list,\
        srv_db_meta_muscian_list
    from db_base_metadata_music_video import srv_db_meta_music_video_lookup,\
        srv_db_meta_music_video_add,\
        srv_db_meta_music_video_detail_by_uuid,\
        srv_db_meta_music_video_count,\
        srv_db_meta_music_video_list
    from db_base_nas import srv_db_nas_count,\
        srv_db_nas_list,\
        srv_db_nas_insert,\
        srv_db_nas_update,\
        srv_db_nas_delete,\
        srv_db_nas_read
    from db_base_metadata_people import srv_db_meta_person_list_count,\
        srv_db_meta_person_list,\
        srv_db_meta_person_by_guid,\
        srv_db_meta_person_by_name,\
        srv_db_meta_person_insert_cast_crew,\
        srv_db_metdata_person_insert,\
        srv_db_meta_person_id_count,\
        srv_db_meta_person_as_seen_in
    from db_base_metadata_sports import srv_db_meta_sports_guid_by_thesportsdb,\
        srv_db_meta_sports_list_count,\
        srv_db_meta_sports_list,\
        srv_db_meta_sports_guid_by_event_name
    from db_base_metadata_thesportsdb import srv_db_metathesportsdb_insert,\
        srv_db_metathesports_update,\
        srv_db_metathesportsdb_select_by_guid
    from db_base_metadata_thetvdb import srv_db_metatvdb_insert,\
        srv_db_metatvdb_update
    from db_base_metadata_tv import srv_db_metatv_guid_by_imdb,\
        srv_db_metatv_guid_by_tvdb,\
        srv_db_metatv_guid_by_tvmaze,\
        srv_db_meta_tvshow_list_count,\
        srv_db_meta_tvshow_list,\
        srv_db_meta_tvshow_detail,\
        srv_db_read_tvmetadata_episodes,\
        srv_db_metatv_guid_by_tvshow_name,\
        srv_db_meta_tvshow_update_image,\
        srv_db_meta_tvshow_images_to_update,\
        srv_db_read_tvmetadata_eps_season,\
        srv_db_read_tvmetadata_season_eps_list,\
        srv_db_read_tvmetadata_episode
    from db_base_metadata_tvmaze import srv_db_meta_tvmaze_changed_uuid,\
        srv_db_meta_tvmaze_insert,\
        srv_db_meta_tvmaze_update
    from db_base_notification import srv_db_notification_insert,\
        srv_db_notification_read
    from db_base_option_status import srv_db_option_status_read,\
        srv_db_option_status_update,\
        srv_db_option_status_update_scan_json,\
        srv_db_option_status_update_scan_json_rec
    from db_base_postgresql import srv_db_pgsql_table_sizes,\
        srv_db_pgsql_row_count,\
        srv_db_pgsql_vacuum_stat_by_day,\
        srv_db_pgsql_vacuum_table
    from db_base_review import srv_db_review_count,\
        srv_db_review_list_by_tmdb_guid,\
        srv_db_review_insert
    from db_base_sync import srv_db_sync_list_count,\
        srv_db_sync_list,\
        srv_db_sync_insert,\
        srv_db_sync_delete,\
        srv_db_sync_progress_update
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
        srv_db_tv_stations_read_stationid_list,\
        srv_db_tv_station_insert,\
        srv_db_tv_station_exist,\
        srv_db_tv_station_update,\
        srv_db_tv_schedule_insert,\
        srv_db_tv_program_insert,\
        srv_db_tv_schedule_by_date
    from db_base_usage import srv_db_usage_top10_alltime,\
        srv_db_usage_top10_movie,\
        srv_db_usage_top10_tv_show,\
        srv_db_usage_top10_tv_episode
    from db_base_users import srv_db_user_list_name_count,\
        srv_db_user_list_name,\
        srv_db_user_detail,\
        srv_db_user_delete,\
        srv_db_user_login_kodi

    # class variables
    sql3_conn = None
    sql3_cursor = None
