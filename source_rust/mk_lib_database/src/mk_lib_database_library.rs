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