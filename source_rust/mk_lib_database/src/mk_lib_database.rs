use std::env;
use std::fs;
use std::path::Path;
use sys_info;
use tokio_postgres::{Error, NoTls};

pub async fn mk_lib_database_open() -> Result<tokio_postgres::Client, Error> {
    // trim is get rid of the \r returned in hostname
    let hostname: String = sys_info::hostname().unwrap().trim().to_string();
    let connection_string: String;
    if hostname == "wsripper2" {
        connection_string = "postgresql://postgres:metaman@localhost/postgres".to_string();
    }
    else {
        if Path::new("/run/secrets/db_password").exists() {
            let dp_pass = fs::read_to_string("/run/secrets/db_password").unwrap();
            connection_string = format!("postgresql://postgres:{}@mkstack_database/postgres",
                                        dp_pass);
        }
        else {
            let dp_pass = env::var("POSTGRES_PASSWORD").unwrap();
            connection_string = format!("postgresql://postgres:{}@mkstack_database/postgres",
                                        dp_pass);
        }
    }
    let (client, connection) = tokio_postgres::connect(&connection_string, NoTls).await?;
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });
    Ok(client)
}

pub async fn mk_lib_database_options(client: tokio_postgres::Client) -> Result<(), Error> {
    let row = client
        .query_one("select mm_options_json from mm_options_and_status", &[])
        .await?;
    let mm_options_json: &str = row.try_get::<&str, serde_json::Value>("mm_options_json")?;
    Ok(mm_options_json)
}

pub async fn mk_lib_database_status(client: tokio_postgres::Client) -> Result<(), Error> {
    let row = client
        .query_one("select mm_status_json from mm_options_and_status", &[])
        .await?;
    let mm_status_json: &str = row.try_get::<&str, serde_json::Value>("mm_status_json")?;
    Ok(mm_status_json)
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