use tokio_postgres::{Error, NoTls};

pub async fn mk_lib_database_open(database_password: &str) -> Result<(), Error> {
    let mut client = tokio_postgres::connect(
        "postgresql://postgres:metaman@mkstack_database/postgres", NoTls)?;
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });
}

pub async fn mk_lib_database_options() -> Result<(), Error> {
    let row = client
        .query_one("select mm_options_json from mm_options_and_status")
        .await?;
    let mm_options_json: &str = row.try_get::<&str, serde_json::Value>("mm_options_json");
}

pub async fn mk_lib_database_status() -> Result<(), Error> {
    let row = client
        .query_one("select mm_status_json from mm_options_and_status")
        .await?;
    let mm_status_json: &str = row.try_get::<&str, serde_json::Value>("mm_status_json");
}