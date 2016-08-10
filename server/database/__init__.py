class MK_Server_Database(object):
    from db_base import MK_Server_Database_Open,\
        MK_Server_Database_Open_Isolation,\
        MK_Server_Database_Close,\
        MK_Server_Database_Commit,\
        MK_Server_Database_Rollback,\
        MK_Server_Database_Table_Index_Check,\
        MK_Server_Database_Table_Count,\
        MK_Server_Database_Query
    from db_base_activity import MK_Server_Database_Activity_Insert,\
        MK_Server_Database_Activity_Purge
    from db_base_audit import MK_Server_Database_Audit_Path_Status,\
        MK_Server_Database_Audit_Path_Update_Status,\
        MK_Server_Database_Audit_Paths_Count,\
        MK_Server_Database_Audit_Path_Update_By_UUID,\
        MK_Server_Database_Audit_Path_Add,\
        MK_Server_Database_Audit_Path_Check,\
        MK_Server_Database_Audit_Directory_Timestamp_Update,\
        MK_Server_Database_Audit_Paths,\
        MK_Server_Database_Audit_Path_Delete,\
        MK_Server_Database_Audit_Path_By_UUID
    from db_base_channel import MK_Server_Database_Channel_Insert
    from db_base_collection import MK_Server_Database_Media_Collection_Scan,\
        MK_Server_Database_Collection_GUID_By_Name,\
        MK_Server_Database_Collection_Insert,\
        MK_Server_Database_Collection_Update,\
        MK_Server_Database_Collection_List,\
        MK_Server_Database_Collection_Read_By_GUID,\
        MK_Server_Database_Collection_By_TMDB
    from db_base_cron import MK_Server_Database_Cron_List_Count,\
        MK_Server_Database_Cron_List,\
        MK_Server_Database_Cron_Time_Update
    from db_base_device import MK_Server_Database_Device_Count,\
        MK_Server_Database_Device_List,\
        MK_Server_Database_Device_Insert,\
        MK_Server_Database_Device_Update,\
        MK_Server_Database_Device_Delete,\
        MK_Server_Database_Device_Read
    from db_base_download import MK_Server_Database_Download_Insert,\
        MK_Server_Database_Download_Read_By_Provider,\
        MK_Server_Database_Download_Delete,\
        MK_Server_Database_Download_Update_Provider,\
        MK_Server_Database_Download_Update
    from db_base_kodi import MK_Server_Database_Kodi_User_Sync,\
        MK_Server_Database_Kodi_User_Sync_List_Added
    from db_base_iradio import MK_Server_Database_iRadio_Insert,\
        MK_Server_Database_iRadio_List_Count,\
        MK_Server_Database_iRadio_List
    from db_base_link import MK_Server_Database_Link_List_Count,\
        MK_Server_Database_Link_List,\
        MK_Server_Database_Link_Insert,\
        MK_Server_Database_Link_Delete
    from db_base_media_class import MK_Server_Database_Media_Class_List_Count,\
        MK_Server_Database_Media_Class_List,\
        MK_Server_Database_Media_Class_By_UUID,\
        MK_Server_Database_Media_UUID_By_Class
    from db_base_media_games import MK_Common_Media_Game_System_List_Count,\
        MK_Common_Media_Game_System_List,\
        MK_Common_Media_Game_List_By_System_Count,\
        MK_Common_Media_Game_List_By_System,\
        MK_Common_Media_Game_List_Count,\
        MK_Common_Media_Game_List
    from db_base_media_images import MK_Common_Media_Images_List_Count,\
        MK_Common_Media_Images_List
    from db_base_media import MK_Server_Database_Insert_Media,\
        MK_Server_Database_Read_Media,\
        MK_Server_Database_Known_Media_Count,\
        MK_Server_Database_Known_Media,\
        MK_Server_Database_Matched_Media_Count,\
        MK_Server_Database_Known_Media_All_Unmatched_Count,\
        MK_Server_Database_Known_Media_All_Unmatched,\
        MK_Server_Database_Media_Duplicate_Count,\
        MK_Server_Database_Media_Duplicate,\
        MK_Server_Database_Media_Duplicate_Detail_Count,\
        MK_Server_Database_Media_Duplicate_Detail,\
        MK_Server_Database_Media_Path_By_UUID,\
        MK_Server_Database_Media_Watched_Status_Update,\
        MK_Server_Database_Update_Media_ID,\
        MK_Server_Database_Update_Media_JSON,\
        MK_Server_Database_Known_Media_Chapter_Scan,\
        MK_Server_Database_Media_By_Metadata_Guid,\
        MK_Server_Database_Media_Image_Path,\
        MK_Server_Database_Read_Media_Metadata_Both,\
        MK_Server_Database_Read_Media_Path_Like,\
        MK_Server_Database_Read_Media_New,\
        MK_Server_Database_Read_Media_New_Count,\
        MK_Server_Database_Media_Watched_Checkpoint_Update,\
        MK_Server_Database_Media_Favorite_Status_Update,\
        MK_Server_Database_Media_Poo_Status_Update,\
        MK_Server_Database_Media_Mismatch_Status_Update
    from db_base_media_movie import MK_Server_Database_Web_Media_List_Count,\
        MK_Server_Database_Media_Movie_Count_By_Genre,\
        MK_Server_Database_Web_Media_List,\
        MK_Server_Database_Media_Random
    from db_base_media_music import MK_Server_Database_Media_Album_Count,\
        MK_Server_Database_Media_Album_List
    from db_base_media_remote import MK_Server_Database_Insert_Remote_Media,\
        MK_Server_Database_Read_Remote_Media,\
        MK_Server_Database_Known_Remote_Media_Count,\
        MK_Server_Database_Media_Remote_Read_New
    from db_base_media_tv import MK_Server_Database_Web_TVMedia_List,\
        MK_Server_Database_Web_TVMedia_List_Count
    from db_base_metadata import MK_Server_Database_Read_Media_Metadata,\
        MK_Server_Database_Metadata_Genre_List_Count,\
        MK_Server_Database_Metadata_Genre_List,\
        MK_Server_Database_Metadata_Movie_Count_By_Genre,\
        MK_Server_Database_Metadata_GUID_By_IMDB,\
        MK_Server_Database_Metadata_GUID_By_TVDB,\
        MK_Server_Database_Metadata_GUID_By_TMDB,\
        MK_Server_Database_Metadata_GUID_By_RT,\
        MK_Server_Database_Metadata_Insert_TMDB,\
        MK_Server_Database_Metadata_TMDB_Count,\
        MK_Server_Database_Metadata_Movie_List,\
        MK_Server_Database_Metadata_Fetch_Media_ID_Json,\
        MK_Server_Database_Metadata_Fetch_Series_Media_ID_Json,\
        MK_Server_Database_Find_Metadata_GUID,\
        MK_Server_Database_Metadata_Update_Media_ID_From_Scudlee
    from db_base_metadata_book import MK_Server_Database_MetadataBook_GUID_By_ISBN,\
        MK_Server_Database_MetadataBook_GUID_By_Name,\
        MK_Server_Database_MetadataBook_Book_Insert
    from db_base_metadata_games import MK_Server_Database_Metadata_Game_System_By_GUID,\
        MK_Server_Database_Metadata_Game_System_List_Count,\
        MK_Server_Database_Metadata_Game_System_List,\
        MK_Server_Database_Metadata_Game_List_Count,\
        MK_Server_Database_Metadata_Game_List,\
        MK_Server_Database_Metadata_Game_By_GUID
    from db_base_metadata_gamesdb import MK_Server_Database_Metadata_GamesDB_System_Insert
    from db_base_metadata_movie import MK_Server_Database_Metadata_Movie_Update_CastCrew
    from db_base_metadata_music import MK_Server_Database_Music_Lookup,\
        MK_Server_Database_Metadata_Musician_By_GUID,\
        MK_Server_Database_Metadata_Musician_Add,\
        MK_Server_Database_Metadata_Album_By_GUID,\
        MK_Server_Database_Metadata_Album_Add,\
        MK_Server_Database_Metadata_Song_By_GUID,\
        MK_Server_Database_Metadata_Song_Add,\
        MK_Server_Database_Metadata_Songs_By_Album_GUID,\
        MK_Server_Database_Metadata_Album_List,\
        MK_Server_Database_Metadata_Muscian_List
    from db_base_metadata_music_video import MK_Server_Database_Metadata_Music_Video_Lookup,\
        MK_Server_Database_Metadata_Music_Video_Add,\
        MK_Server_Database_Metadata_Music_Video_Detail_By_UUID,\
        MK_Server_Database_Metadata_Music_Video_Count,\
        MK_Server_Database_Metadata_Music_Video_List
    from db_base_nas import MK_Server_Database_NAS_Count,\
        MK_Server_Database_NAS_List,\
        MK_Server_Database_NAS_Insert,\
        MK_Server_Database_NAS_Update,\
        MK_Server_Database_NAS_Delete,\
        MK_Server_Database_NAS_Read
    from db_base_metadata_people import MK_Server_Database_Metadata_Person_List_Count,\
        MK_Server_Database_Metadata_Person_List,\
        MK_Server_Database_Metadata_Person_By_GUID,\
        MK_Server_Database_Metadata_Person_By_Name,\
        MK_Server_Database_Metadata_Person_Insert_Cast_Crew,\
        MK_Server_Database_Metdata_Person_Insert,\
        MK_Server_Database_Metadata_Person_ID_Count,\
        MK_Server_Database_Metadata_Person_As_Seen_In
    from db_base_metadata_sports import MK_Server_Database_Metadata_Sports_GUID_By_TheSportsDB,\
        MK_Server_Database_Metadata_Sports_List_Count,\
        MK_Server_Database_Metadata_Sports_List,\
        MK_Server_Database_Metadata_Sports_GUID_By_Event_Name
    from db_base_metadata_thesportsdb import MK_Server_Database_MetadataTheSportsDB_Insert,\
        MK_Server_Database_MetadataTheSports_Update,\
        MK_Server_Database_MetadataTheSportsDB_Select_By_Guid
    from db_base_metadata_thetvdb import MK_Server_Database_MetadataTVDB_Insert,\
        MK_Server_Database_MetadataTVDB_Update
    from db_base_metadata_tv import MK_Server_Database_MetadataTV_GUID_By_IMDB,\
        MK_Server_Database_MetadataTV_GUID_By_TVDB,\
        MK_Server_Database_MetadataTV_GUID_By_TVMaze,\
        MK_Server_Database_Metadata_TVShow_List_Count,\
        MK_Server_Database_Metadata_TVShow_List,\
        MK_Server_Database_Metadata_TVShow_Detail,\
        MK_Server_Database_Read_TVMetadata_Episodes,\
        MK_Server_Database_MetadataTV_GUID_By_TVShow_Name,\
        MK_Server_Database_Metadata_TVShow_Update_Image,\
        MK_Server_Database_Metadata_TVShow_Images_To_Update,\
        MK_Server_Database_Read_TVMetadata_Eps_Season,\
        MK_Server_Database_Read_TVMetadata_Season_Eps_List,\
        MK_Server_Database_Read_TVMetadata_Episode
    from db_base_metadata_tvmaze import MK_Server_Database_MetadataTVMaze_Changed_UUID,\
        MK_Server_Database_MetadataTVMaze_Insert,\
        MK_Server_Database_MetadataTVMaze_Update
    from db_base_notification import MK_Server_Database_Notification_Insert,\
        MK_Server_Database_Notification_Read
    from db_base_option_status import MK_Server_Database_Option_Status_Read,\
        MK_Server_Database_Option_Status_Update,\
        MK_Server_Database_Option_Status_Update_Scan_Json,\
        MK_Server_Database_Option_Status_Update_Scan_Json_Rec
    from db_base_postgresql import MK_Server_Database_Postgresql_Table_Sizes,\
        MK_Server_Database_Postgresql_Row_Count,\
        MK_Server_Database_Postgresql_Vacuum_Stat_By_Day,\
        MK_Server_Database_Postgresql_Vacuum_Table
    from db_base_review import MK_Server_Database_Review_Count,\
        MK_Server_Database_Review_List_By_TMDB_GUID,\
        MK_Server_Database_Review_Insert
    from db_base_sync import MK_Server_Database_Sync_List_Count,\
        MK_Server_Database_Sync_List,\
        MK_Server_Database_Sync_Insert,\
        MK_Server_Database_Sync_Delete,\
        MK_Server_Database_Sync_Progress_Update
    from db_base_triggers import MK_Server_Database_Trigger_Insert,\
        MK_Server_Database_Triggers_Read,\
        MK_Server_Database_Triggers_Delete
    from db_base_tuner import MK_Server_Database_Tuner_Count,\
        MK_Server_Database_Tuner_Insert,\
        MK_Server_Database_Tuner_Delete,\
        MK_Server_Database_Tuner_List,\
        MK_Server_Database_Tuner_By_Serial,\
        MK_Server_Database_Tuner_Update
    from db_base_tv_schedule import MK_Server_Database_TV_Stations_Read,\
        MK_Server_Database_TV_Stations_Read_StationID_List,\
        MK_Server_Database_TV_Station_Insert,\
        MK_Server_Database_TV_Station_Exist,\
        MK_Server_Database_TV_Station_Update,\
        MK_Server_Database_TV_Schedule_Insert,\
        MK_Server_Database_TV_Program_Insert,\
        MK_Server_Database_TV_Schedule_By_Date
    from db_base_usage import MK_Server_Database_Usage_Top10_AllTime,\
        MK_Server_Database_Usage_Top10_Movie,\
        MK_Server_Database_Usage_Top10_TV_Show,\
        MK_Server_Database_Usage_Top10_TV_Episode
    from db_base_users import MK_Server_Database_User_List_Name_Count,\
        MK_Server_Database_User_List_Name,\
        MK_Server_Database_User_Detail,\
        MK_Server_Database_User_Delete,\
        MK_Server_Database_User_Login_Kodi

    # class variables
    sql3_conn = None
    sql3_cursor = None
