use tokio_postgres::Error;
use uuid::Uuid;

pub async fn mk_lib_database_media_insert(client: &tokio_postgres::Client,
                                             mm_media_guid: Uuid,
                                             mm_media_class_guid: i16,
                                             mm_media_path: String,
                                             mm_media_metadata_guid: Uuid,
                                             mm_media_ffprobe_json: String,
                                             mm_media_json: String)
                                             -> Result<bool, Error> {
    client
        .query_one("insert into mm_media (mm_media_guid, mm_media_class_guid,\
         mm_media_path, mm_media_metadata_guid, mm_media_ffprobe_json, mm_media_json)\
          values ($1, $2, $3, $4, $5, $6)",
                   &[&mm_media_guid, &mm_media_class_guid, &mm_media_path,
                       &mm_media_metadata_guid, &mm_media_ffprobe_json, &mm_media_json]).await?;
    Ok()
}
