use tokio::time::{Duration, sleep};

pub static DATABASE_VERSION: u32 = 43;

pub async fn mk_lib_database_version(client: &tokio_postgres::Client) -> Result<i32, Error> {
    let row = client
        .query_one("select mm_version_no from mm_version", &[])
        .await?;
    Ok(row.get("mm_version_no"))
}

pub async fn mk_lib_database_version_check(client: &tokio_postgres::Client,
                                           must_match: bool) -> Result<bool, Error> {
    let row = client
        .query_one("select mm_version_no from mm_version", &[])
        .await?;
    let mut version_match: bool = false;
    if DATABASE_VERSION == row.get("mm_version_no") {
        version_match = true;
    }
    if must_match && version_match == false {
        loop {
            sleep(Duration::from_secs(5)).await;
            let row = client
                .query_one("select mm_version_no from mm_version", &[])
                .await?;
            if DATABASE_VERSION == row.get("mm_version_no") {
                version_match = true;
                break;
            }
        }
    }
    Ok(version_match)
}

pub async fn mk_lib_database_version_update(client: &tokio_postgres::Client,
                                            version_number: i32) -> Result<(), Error> {
    client
        .query("update mm_version set mm_version_no = $1", &[&version_number])
        .await?;
    Ok(())
}