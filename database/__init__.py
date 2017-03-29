class MKServerDatabase(object):
    """
    Main database class for server
    """
    from database.db_base import db_open,\
        db_close,\
        db_commit,\
        db_rollback,\
        db_table_index_check,\
        db_table_count,\
        db_query
    from database.db_base_activity import db_activity_insert,\
        db_activity_purge
    from database.db_base_audit import db_audit_path_status,\
        db_audit_path_update_status,\
        db_audit_path_update_by_uuid,\
        db_audit_path_add,\
        db_audit_path_check,\
        db_audit_dir_timestamp_update,\
        db_audit_paths,\
        db_audit_path_delete,\
        db_audit_path_by_uuid,\
        db_audit_shares,\
        db_audit_share_delete,\
        db_audit_share_by_uuid,\
        db_audit_share_update_by_uuid,\
        db_audit_share_check,\
        db_audit_share_add
    from database.db_base_channel import db_channel_insert
    from database.db_base_collection import db_media_collection_scan,\
        db_collection_guid_by_name,\
        db_collection_insert,\
        db_collection_update,\
        db_collection_list,\
        db_collection_read_by_guid,\
        db_collection_by_tmdb
    from database.db_base_cron import db_cron_list_count,\
        db_cron_list,\
        db_cron_time_update,\
        db_cron_insert
    from database.db_base_device import db_device_count,\
        db_device_list,\
        db_device_insert,\
        db_device_update,\
        db_device_delete,\
        db_device_read
    from database.db_base_download import db_download_insert,\
        db_download_read_provider,\
        db_download_delete,\
        db_download_update_provider,\
        db_download_update,\
        db_download_que_exists
    from database.db_base_download_images import db_download_image_insert,\
        db_download_image_read,\
        db_download_image_delete
    from database.db_base_kodi import db_kodi_user_sync_movie,\
        db_kodi_user_sync_added,\
        db_kodi_user_sync_collection,\
        db_kodi_user_sync_tv_shows,\
        db_kodi_user_sync_music_videos,\
        db_kodi_user_sync_tv_seasons,\
        db_kodi_user_sync_tv_episodes,\
        db_kodi_user_sync_music_artists,\
        db_kodi_user_sync_music_albums,\
        db_kodi_user_sync_music_songs
    from database.db_base_iradio import db_iradio_insert,\
        db_iradio_list_count,\
        db_iradio_list
    from database.db_base_link import db_link_list_count,\
        db_link_list,\
        db_link_insert,\
        db_link_delete
    from database.db_base_media_books import db_media_book_list_count,\
        db_media_book_list
    from database.db_base_media_class import db_media_class_list_count,\
        db_media_class_insert,\
        db_media_class_list,\
        db_media_class_by_uuid,\
        db_media_uuid_by_class
    from database.db_base_media_games import db_media_game_system_list_count,\
        db_media_game_system_list,\
        db_media_game_list_by_system_count,\
        db_media_game_list_by_system,\
        db_media_game_list_count,\
        db_media_game_list
    from database.db_base_media_images import db_media_images_list_count,\
        db_media_images_list
    from database.db_base_media import db_insert_media,\
        db_read_media,\
        db_known_media_count,\
        db_known_media,\
        db_matched_media_count,\
        db_known_media_all_unmatched_count,\
        db_known_media_all_unmatched,\
        db_media_duplicate_count,\
        db_media_duplicate,\
        db_media_duplicate_detail_count,\
        db_media_duplicate_detail,\
        db_media_path_by_uuid,\
        db_media_watched_status_update,\
        db_update_media_id,\
        db_update_media_json,\
        db_known_media_chapter_scan,\
        db_media_by_metadata_guid,\
        db_media_image_path,\
        db_read_media_metadata_both,\
        db_read_media_path_like,\
        db_read_media_new,\
        db_read_media_new_count,\
        db_media_watched_checkpoint_update,\
        db_media_favorite_status_update,\
        db_media_poo_status_update,\
        db_media_mismatch_status_update,\
        db_read_media_ffprobe,\
        db_media_ffmeg_update
    from database.db_base_media_movie import db_web_media_list_count,\
        db_media_movie_count_by_genre,\
        db_web_media_list,\
        db_media_random
    from database.db_base_media_music import db_media_album_count,\
        db_media_album_list
    from database.db_base_media_music_video import db_music_video_list
    from database.db_base_media_remote import db_insert_remote_media,\
        db_read_remote_media,\
        db_known_remote_media_count,\
        db_media_remote_read_new
    from database.db_base_media_tv import db_web_tvmedia_list,\
        db_web_tvmedia_list_count
    from database.db_base_metadata import db_read_media_metadata,\
        db_meta_genre_list_count,\
        db_meta_genre_list,\
        db_meta_movie_count_genre,\
        db_meta_guid_by_imdb,\
        db_meta_guid_by_tvdb,\
        db_meta_guid_by_tmdb,\
        db_meta_guid_by_rt,\
        db_meta_insert_tmdb,\
        db_meta_tmdb_count,\
        db_meta_movie_list,\
        db_meta_fetch_media_id_json,\
        db_meta_fetch_series_media_id_json,\
        db_find_metadata_guid,\
        db_meta_update_media_id_from_scudlee
    from database.db_base_metadata_anime import db_meta_anime_title_insert,\
        db_meta_anime_title_search,\
        db_meta_anime_update_meta_id,\
        db_meta_anime_meta_by_id
    from database.db_base_metadata_book import db_meta_book_list,\
        db_meta_book_guid_by_isbn,\
        db_meta_book_guid_by_name,\
        db_meta_book_insert,\
        db_meta_book_by_uuid
    from database.db_base_metadata_games import db_meta_game_system_by_guid,\
        db_meta_game_system_list_count,\
        db_meta_game_system_list,\
        db_meta_game_list_count,\
        db_meta_game_list,\
        db_meta_game_by_guid,\
        db_meta_games_system_insert
    from database.db_base_metadata_movie import db_meta_movie_update_castcrew
    from database.db_base_metadata_music import db_music_lookup,\
        db_meta_musician_by_guid,\
        db_meta_musician_add,\
        db_meta_album_by_guid,\
        db_meta_album_add,\
        db_meta_song_by_guid,\
        db_meta_song_add,\
        db_meta_songs_by_album_guid,\
        db_meta_song_list,\
        db_meta_album_list,\
        db_meta_muscian_list
    from database.db_base_metadata_music_video import db_meta_music_video_lookup,\
        db_meta_music_video_add,\
        db_meta_music_video_detail_uuid,\
        db_meta_music_video_count,\
        db_meta_music_video_list
    from database.db_base_nas import db_nas_count,\
        db_nas_list,\
        db_nas_insert,\
        db_nas_update,\
        db_nas_delete,\
        db_nas_read
    from database.db_base_metadata_people import db_meta_person_list_count,\
        db_meta_person_list,\
        db_meta_person_by_guid,\
        db_meta_person_by_name,\
        db_meta_person_insert_cast_crew,\
        db_meta_person_insert,\
        db_meta_person_update,\
        db_meta_person_id_count,\
        db_meta_person_as_seen_in
    from database.db_base_metadata_sports import db_meta_sports_guid_by_thesportsdb,\
        db_meta_sports_list_count,\
        db_meta_sports_list,\
        db_meta_sports_guid_by_event_name
    from database.db_base_metadata_thesportsdb import db_metathesportsdb_insert,\
        db_metathesports_update,\
        db_metathesportsdb_select_guid
    from database.db_base_metadata_thetvdb import db_metatvdb_insert,\
        db_metatvdb_update
    from database.db_base_metadata_tv import db_metatv_guid_by_imdb,\
        db_metatv_guid_by_tvdb,\
        db_metatv_guid_by_tvmaze,\
        db_metatv_guid_by_tmdb,\
        db_metatv_guid_by_rt,\
        db_meta_tvshow_list_count,\
        db_meta_tvshow_list,\
        db_meta_tvshow_detail,\
        db_read_tvmeta_episodes,\
        db_metatv_guid_by_tvshow_name,\
        db_meta_tvshow_update_image,\
        db_meta_tvshow_images_to_update,\
        db_read_tvmeta_eps_season,\
        db_read_tvmeta_season_eps_list,\
        db_read_tvmeta_episode
    from database.db_base_metadata_tvmaze import db_meta_tvmaze_changed_uuid,\
        db_meta_tvmaze_insert,\
        db_meta_tvmaze_update
    from database.db_base_notification import db_notification_insert,\
        db_notification_read,\
        db_notification_delete
    from database.db_base_option_status import db_opt_status_read,\
        db_opt_status_update,\
        db_opt_status_update_scan,\
        db_opt_status_update_scan_rec,\
        db_opt_status_insert
    from database.db_base_postgresql import db_pgsql_table_sizes,\
        db_pgsql_row_count,\
        db_pgsql_vacuum_stat_by_day,\
        db_pgsql_vacuum_table,\
        db_pgsql_set_iso_level,\
        db_pgsql_table_exits
    from database.db_base_review import db_review_count,\
        db_review_list_by_tmdb_guid,\
        db_review_insert
    from database.db_base_sync import db_sync_list_count,\
        db_sync_list,\
        db_sync_insert,\
        db_sync_delete,\
        db_sync_progress_update
    from database.db_base_triggers import db_trigger_insert,\
        db_triggers_read,\
        db_triggers_delete
    from database.db_base_tuner import db_tuner_count,\
        db_tuner_insert,\
        db_tuner_delete,\
        db_tuner_list,\
        db_tuner_by_serial,\
        db_tuner_update
    from database.db_base_tv_schedule import db_tv_stations_read,\
        db_tv_stations_read_stationid_list,\
        db_tv_station_insert,\
        db_tv_station_exist,\
        db_tv_station_update,\
        db_tv_schedule_insert,\
        db_tv_program_insert,\
        db_tv_schedule_by_date
    from database.db_base_usage import db_usage_top10_alltime,\
        db_usage_top10_movie,\
        db_usage_top10_tv_show,\
        db_usage_top10_tv_episode
    from database.db_base_users import db_user_list_name_count,\
        db_user_list_name,\
        db_user_detail,\
        db_user_delete,\
        db_user_login_kodi,\
        db_user_group_insert,\
        db_user_profile_insert
    from database.db_base_version import db_version_check,\
        db_version_update

    # class variables
    sql3_conn = None
    sql3_cursor = None
