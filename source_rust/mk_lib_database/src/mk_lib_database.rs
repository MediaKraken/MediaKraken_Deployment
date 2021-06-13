use tokio_postgres::{Error, NoTls};

pub async fn mk_lib_database_open(database_password: &str)
                                  -> Result<tokio_postgres::Client, Error> {
    let (client, connection) = tokio_postgres::connect(
        format!("postgresql://postgres:{}@mkstack_database/postgres",
                database_password).as_str(), NoTls).await?;
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });
    Ok(client)
}

// pub async fn mk_lib_database_options(client: tokio_postgres::Client) -> Result<(), Error> {
//     let row = client
//         .query_one("select mm_options_json from mm_options_and_status", &[])
//         .await?;
//     let mm_options_json: &str = row.try_get::<&str, serde_json::Value>("mm_options_json")?;
// }
//
// pub async fn mk_lib_database_status(client: tokio_postgres::Client) -> Result<(), Error> {
//     let row = client
//         .query_one("select mm_status_json from mm_options_and_status", &[])
//         .await?;
//     let mm_status_json: &str = row.try_get::<&str, serde_json::Value>("mm_status_json")?;
// }

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