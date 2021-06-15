use serde::{Deserialize, Serialize};
use std::error::Error;

#[path = "../../mk_lib_common/src/mk_lib_common.rs"]
mod mk_lib_common;
#[path = "../../mk_lib_common/src/mk_lib_common_enum_media_type.rs"]
mod mk_lib_common_enum_media_type;
#[path = "../../mk_lib_compression/src/mk_lib_compression.rs"]
mod mk_lib_compression;
#[path = "../../mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;
#[path = "../../mk_lib_database/src/mk_lib_database_download.rs"]
mod mk_lib_database_download;
#[path = "../../mk_lib_database/src/mk_lib_database_metadata.rs"]
mod mk_lib_database_metadata;
#[path = "../../mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[path = "../../mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_networks;

#[derive(Serialize, Deserialize)]
struct MetadataMovie {
    adult: bool,
    id: i32,
    original_title: String,
    popularity: f32,
    video: bool,
}

#[derive(Serialize, Deserialize)]
struct MetadataTV {
    id: i32,
    original_name: String,
    popularity: f32,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        "bulk_themoviedb_netfetch").await;

    let fetch_date: String = "06_11_2021".to_string();

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    // grab the movie id's
    // let _fetch_result = mk_lib_networks::mk_download_file_from_url(
    //     format!("http://files.tmdb.org/p/exports/movie_ids_{}.json.gz", fetch_date),
    //     "movie.gz".to_string());
    let json_result = mk_lib_compression::mk_decompress_gzip("movie.gz").unwrap();
    // Please note that the data is NOT in id order
    for json_item in json_result.split('\n') {
        let metadata_struct: MetadataMovie = serde_json::from_str(json_item)?;
        let result = mk_lib_database_metadata::mk_lib_database_metadata_exists_movie(db_client,
                                                                                     metadata_struct.id).await.unwrap();
        if result == false {
            println!("waffles! {}", metadata_struct.id)
        }
    }

    // grab the TV id's
    // let _fetch_result = mk_lib_networks::mk_download_file_from_url(
    //     format!("http://files.tmdb.org/p/exports/tv_series_ids_{}.json.gz", fetch_date),
    //     "tv.gz".to_string());
    let json_result = mk_lib_compression::mk_decompress_gzip("tv.gz").unwrap();
    for json_item in json_result.split('\n') {
        let metadata_struct: MetadataTV = serde_json::from_str(json_item)?;
        let result = mk_lib_database_metadata::mk_lib_database_metadata_exists_tv(db_client,
                                                                                  metadata_struct.id).await.unwrap();
        if result == false {
            println!("waffles! {}", metadata_struct.id)
        }
    }

    // let name = "Ferris";
    // let data = None::<&[u8]>;
    // client.execute(
    //     "INSERT INTO person (name, data) VALUES ($1, $2)",
    //     &[&name, &data],
    // )?;
    //
    // for row in client.query("SELECT id, name, data FROM person", &[])? {
    //     let id: i32 = row.get(0);
    //     let name: &str = row.get(1);
    //     let data: Option<&[u8]> = row.get(2);
    //     println!("found person: {} {} {:?}", id, name, data);
    // }

    // stop logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        "bulk_themoviedb_netfetch").await;
    Ok(())
}