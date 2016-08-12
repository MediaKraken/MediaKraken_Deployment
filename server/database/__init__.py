class MK_Server_Database(object):
    from db_base import srv_db_Open,\
        srv_db_Open_Isolation,\
        srv_db_Close,\
        srv_db_Commit,\
        srv_db_Rollback,\
        srv_db_Table_Index_Check,\
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
    from db_base_collection import srv_db_Media_Collection_Scan,\
        srv_db_Collection_GUID_By_Name,\
        srv_db_Collection_Insert,\
        srv_db_Collection_Update,\
        srv_db_Collection_List,\
        srv_db_Collection_Read_By_GUID,\
        srv_db_Collection_By_TMDB
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
    from db_base_media_class import srv_db_Media_Class_List_Count,\
        srv_db_Media_Class_List,\
        srv_db_Media_Class_By_UUID,\
        srv_db_Media_UUID_By_Class
    from db_base_media_games import common.common_Media_Game_System_List_Count,\
        com_Media_Game_System_List,\
        com_Media_Game_List_By_System_Count,\
        com_Media_Game_List_By_System,\
        com_Media_Game_List_Count,\
        com_Media_Game_List
    from db_base_media_images import common.common_Media_Images_List_Count,\
        com_Media_Images_List
    from db_base_media import srv_db_Insert_Media,\
        srv_db_Read_Media,\
        srv_db_Known_Media_Count,\
        srv_db_Known_Media,\
        srv_db_Matched_Media_Count,\
        srv_db_Known_Media_All_Unmatched_Count,\
        srv_db_Known_Media_All_Unmatched,\
        srv_db_Media_Duplicate_Count,\
        srv_db_Media_Duplicate,\
        srv_db_Media_Duplicate_Detail_Count,\
        srv_db_Media_Duplicate_Detail,\
        srv_db_Media_Path_By_UUID,\
        srv_db_Media_Watched_Status_Update,\
        srv_db_Update_Media_ID,\
        srv_db_Update_Media_JSON,\
        srv_db_Known_Media_Chapter_Scan,\
        srv_db_Media_By_Metadata_Guid,\
        srv_db_Media_Image_Path,\
        srv_db_Read_Media_Metadata_Both,\
        srv_db_Read_Media_Path_Like,\
        srv_db_Read_Media_New,\
        srv_db_Read_Media_New_Count,\
        srv_db_Media_Watched_Checkpoint_Update,\
        srv_db_Media_Favorite_Status_Update,\
        srv_db_Media_Poo_Status_Update,\
        srv_db_Media_Mismatch_Status_Update
    from db_base_media_movie import srv_db_Web_Media_List_Count,\
        srv_db_Media_Movie_Count_By_Genre,\
        srv_db_Web_Media_List,\
        srv_db_Media_Random
    from db_base_media_music import srv_db_Media_Album_Count,\
        srv_db_Media_Album_List
    from db_base_media_remote import srv_db_Insert_Remote_Media,\
        srv_db_Read_Remote_Media,\
        srv_db_Known_Remote_Media_Count,\
        srv_db_Media_Remote_Read_New
    from db_base_media_tv import srv_db_Web_TVMedia_List,\
        srv_db_Web_TVMedia_List_Count
    from db_base_metadata import srv_db_Read_Media_Metadata,\
        srv_db_Metadata_Genre_List_Count,\
        srv_db_Metadata_Genre_List,\
        srv_db_Metadata_Movie_Count_By_Genre,\
        srv_db_Metadata_GUID_By_IMDB,\
        srv_db_Metadata_GUID_By_TVDB,\
        srv_db_Metadata_GUID_By_TMDB,\
        srv_db_Metadata_GUID_By_RT,\
        srv_db_Metadata_Insert_TMDB,\
        srv_db_Metadata_TMDB_Count,\
        srv_db_Metadata_Movie_List,\
        srv_db_Metadata_Fetch_Media_ID_Json,\
        srv_db_Metadata_Fetch_Series_Media_ID_Json,\
        srv_db_Find_Metadata_GUID,\
        srv_db_Metadata_Update_Media_ID_From_Scudlee
    from db_base_metadata_book import srv_db_MetadataBook_GUID_By_ISBN,\
        srv_db_MetadataBook_GUID_By_Name,\
        srv_db_MetadataBook_Book_Insert
    from db_base_metadata_games import srv_db_Metadata_Game_System_By_GUID,\
        srv_db_Metadata_Game_System_List_Count,\
        srv_db_Metadata_Game_System_List,\
        srv_db_Metadata_Game_List_Count,\
        srv_db_Metadata_Game_List,\
        srv_db_Metadata_Game_By_GUID
    from db_base_metadata_gamesdb import srv_db_Metadata_GamesDB_System_Insert
    from db_base_metadata_movie import srv_db_Metadata_Movie_Update_CastCrew
    from db_base_metadata_music import srv_db_Music_Lookup,\
        srv_db_Metadata_Musician_By_GUID,\
        srv_db_Metadata_Musician_Add,\
        srv_db_Metadata_Album_By_GUID,\
        srv_db_Metadata_Album_Add,\
        srv_db_Metadata_Song_By_GUID,\
        srv_db_Metadata_Song_Add,\
        srv_db_Metadata_Songs_By_Album_GUID,\
        srv_db_Metadata_Album_List,\
        srv_db_Metadata_Muscian_List
    from db_base_metadata_music_video import srv_db_Metadata_Music_Video_Lookup,\
        srv_db_Metadata_Music_Video_Add,\
        srv_db_Metadata_Music_Video_Detail_By_UUID,\
        srv_db_Metadata_Music_Video_Count,\
        srv_db_Metadata_Music_Video_List
    from db_base_nas import srv_db_NAS_Count,\
        srv_db_NAS_List,\
        srv_db_NAS_Insert,\
        srv_db_NAS_Update,\
        srv_db_NAS_Delete,\
        srv_db_NAS_Read
    from db_base_metadata_people import srv_db_Metadata_Person_List_Count,\
        srv_db_Metadata_Person_List,\
        srv_db_Metadata_Person_By_GUID,\
        srv_db_Metadata_Person_By_Name,\
        srv_db_Metadata_Person_Insert_Cast_Crew,\
        srv_db_Metdata_Person_Insert,\
        srv_db_Metadata_Person_ID_Count,\
        srv_db_Metadata_Person_As_Seen_In
    from db_base_metadata_sports import srv_db_Metadata_Sports_GUID_By_TheSportsDB,\
        srv_db_Metadata_Sports_List_Count,\
        srv_db_Metadata_Sports_List,\
        srv_db_Metadata_Sports_GUID_By_Event_Name
    from db_base_metadata_thesportsdb import srv_db_MetadataTheSportsDB_Insert,\
        srv_db_MetadataTheSports_Update,\
        srv_db_MetadataTheSportsDB_Select_By_Guid
    from db_base_metadata_thetvdb import srv_db_MetadataTVDB_Insert,\
        srv_db_MetadataTVDB_Update
    from db_base_metadata_tv import srv_db_MetadataTV_GUID_By_IMDB,\
        srv_db_MetadataTV_GUID_By_TVDB,\
        srv_db_MetadataTV_GUID_By_TVMaze,\
        srv_db_Metadata_TVShow_List_Count,\
        srv_db_Metadata_TVShow_List,\
        srv_db_Metadata_TVShow_Detail,\
        srv_db_Read_TVMetadata_Episodes,\
        srv_db_MetadataTV_GUID_By_TVShow_Name,\
        srv_db_Metadata_TVShow_Update_Image,\
        srv_db_Metadata_TVShow_Images_To_Update,\
        srv_db_Read_TVMetadata_Eps_Season,\
        srv_db_Read_TVMetadata_Season_Eps_List,\
        srv_db_Read_TVMetadata_Episode
    from db_base_metadata_tvmaze import srv_db_MetadataTVMaze_Changed_UUID,\
        srv_db_MetadataTVMaze_Insert,\
        srv_db_MetadataTVMaze_Update
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
        srv_db_Review_Insert
    from db_base_sync import srv_db_Sync_List_Count,\
        srv_db_Sync_List,\
        srv_db_Sync_Insert,\
        srv_db_Sync_Delete,\
        srv_db_Sync_Progress_Update
    from db_base_triggers import srv_db_Trigger_Insert,\
        srv_db_Triggers_Read,\
        srv_db_Triggers_Delete
    from db_base_tuner import srv_db_Tuner_Count,\
        srv_db_Tuner_Insert,\
        srv_db_Tuner_Delete,\
        srv_db_Tuner_List,\
        srv_db_Tuner_By_Serial,\
        srv_db_Tuner_Update
    from db_base_tv_schedule import srv_db_TV_Stations_Read,\
        srv_db_TV_Stations_Read_StationID_List,\
        srv_db_TV_Station_Insert,\
        srv_db_TV_Station_Exist,\
        srv_db_TV_Station_Update,\
        srv_db_TV_Schedule_Insert,\
        srv_db_TV_Program_Insert,\
        srv_db_TV_Schedule_By_Date
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
