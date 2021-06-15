use tokio_postgres::{Error};

pub async fn mk_lib_database_metadata_exists_movie(client: &tokio_postgres::Client,
                                                   metadata_id: i32)
                                                   -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_metadata_movie \
        where mm_metadata_media_id = $1 limit 1) as found_record limit 1",
                   &[&metadata_id]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}

pub async fn mk_lib_database_metadata_exists_person(client: &tokio_postgres::Client,
                                                metadata_id: i32)
                                                -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_metadata_person \
        where mmp_person_media_id = $1 limit 1) as found_record limit 1",
                   &[&metadata_id]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}

pub async fn mk_lib_database_metadata_exists_tv(client: &tokio_postgres::Client,
                                                metadata_id: i32)
                                                -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_metadata_tvshow \
        where mm_metadata_media_tvshow_id = $1 limit 1) as found_record limit 1",
                   &[&metadata_id]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}