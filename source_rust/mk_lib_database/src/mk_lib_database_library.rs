use tokio_postgres::{Error, Row};

pub async fn mk_lib_database_library_read(client: &tokio_postgres::Client)
                                               -> Result<Vec<Row>, Error> {
    let rows = client
        .query("select mm_media_dir_guid, mm_media_dir_path from mm_media_dir", &[])
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