pub async fn mk_lib_database_downloads_exists(client: &tokio_postgres::Client,
                                              metadata_id: i32)
                                              -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_download_que \
        where mdq_provider_id = $1 limit 1) as found_record limit 1",
                   &[&metadata_id]).await?;
    println!("row: {:?}", row);
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