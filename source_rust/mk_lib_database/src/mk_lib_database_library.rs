use tokio_postgres::{Error, Row};

pub async fn mk_lib_database_library_read(client: &tokio_postgres::Client)
                                          -> Result<Vec<Row>, Error> {
    let rows = client
        .query("select mm_media_dir_guid, mm_media_dir_path from mm_media_dir", &[])
        .await?;
    Ok(rows)
}

pub async fn mk_lib_database_library_path_audit(client: &tokio_postgres::Client)
                                                -> Result<Vec<Row>, Error> {
    let rows = client
        .query("select mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, \
        mm_media_dir_last_scanned from mm_media_dir", &[])
        .await?;
    Ok(rows)
}


pub async fn mk_lib_database_library_path_status(client: &tokio_postgres::Client)
                                                 -> Result<Vec<Row>, Error> {
    let rows = client
        .query("select mm_media_dir_path, mm_media_dir_status \
        from mm_media_dir where mm_media_dir_status IS NOT NULL \
        order by mm_media_dir_path", &[])
        .await?;
    Ok(rows)
}


pub async fn mk_lib_database_library_path_status_update(client: &tokio_postgres::Client,
                                                        library_uuid: uuid::Uuid,
                                                        library_status_json: serde_json::Value)
                                                        -> Result<(), Error> {
    client.query("update mm_media_dir set mm_media_dir_status = $1 where mm_media_dir_guid = $2",
                 &[&library_status_json, &library_uuid]).await?;
    Ok(())
}

pub async fn mk_lib_database_library_path_timestamp_update(client: &tokio_postgres::Client,
                                                           library_uuid: uuid::Uuid)
                                                           -> Result<(), Error> {
    client.query("update mm_media_dir set mm_media_dir_last_scanned = NOW() \
     where mm_media_dir_guid = $1)",
                 &[&library_uuid]).await?;
    Ok(())
}

pub async fn mk_lib_database_library_file_exists(client: &tokio_postgres::Client,
                                                 file_name: String)
                                                 -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_media \
        where mm_media_path = $1 limit 1) \
        as found_record limit 1", &[&file_name]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}

// // cargo test -- --show-output
// #[cfg(test)]
// mod test_mk_lib_common {
//     use super::*;
//
//     macro_rules! aw {
//     ($e:expr) => {
//         tokio_test::block_on($e)
//     };
//   }
// }