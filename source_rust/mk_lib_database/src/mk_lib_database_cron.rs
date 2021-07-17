use tokio_postgres::{Error, Row};
use uuid::Uuid;

pub async fn mk_lib_database_cron_service_read(client: &tokio_postgres::Client)
                                               -> Result<Vec<Row>, Error> {
    let rows = client
        .query("select mm_cron_guid, mm_cron_schedule, mm_cron_last_run, \
        mm_cron_json from mm_cron where mm_cron_enabled = true", &[])
        .await?;
    Ok(rows)
}

pub async fn mk_lib_database_cron_time_update(client: &tokio_postgres::Client,
                                              cron_uuid: uuid::Uuid)
                                              -> Result<Vec<Row>, Error> {
    println!("uuid: {:?}", cron_uuid);
    let rows = client
        .query("update mm_cron set mm_cron_last_run = NOW() \
        where mm_cron_guid = $1", &[&cron_uuid])
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