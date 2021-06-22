use serde::{Deserialize, Serialize};
use std::error::Error;
use uuid::Uuid;

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_common/src/mk_lib_common.rs"]
mod mk_lib_common;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_common/src/mk_lib_common_enum_media_type.rs"]
mod mk_lib_common_enum_media_type;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_compression/src/mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_download.rs"]
mod mk_lib_database_download;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_metadata.rs"]
mod mk_lib_database_metadata;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_networks;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_common.rs"]
mod mk_lib_common;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_common_enum_media_type.rs"]
mod mk_lib_common_enum_media_type;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_download.rs"]
mod mk_lib_database_download;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_metadata.rs"]
mod mk_lib_database_metadata;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_network.rs"]
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

    let fetch_date: String = "06_20_2021".to_string();

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    // grab the movie id's
    let _fetch_result_movie = mk_lib_networks::mk_download_file_from_url(
        format!("http://files.tmdb.org/p/exports/movie_ids_{}.json.gz", fetch_date),
        "movie.gz".to_string());
    let json_result = mk_lib_compression::mk_decompress_gzip("movie.gz").unwrap();
    // Please note that the data is NOT in id order
    for json_item in json_result.split('\n') {
        if !json_item.trim().is_empty() {
            let metadata_struct: MetadataMovie = serde_json::from_str(json_item)?;
            let result = mk_lib_database_metadata::mk_lib_database_metadata_exists_movie(db_client,
                                                                                         metadata_struct.id).await.unwrap();
            if result == false {
                let download_result = mk_lib_database_download::mk_lib_database_download_exists(db_client,
                                                                                                "themoviedb".to_string(),
                                                                                                mk_lib_common_enum_media_type::DLMediaType::MOVIE,
                                                                                                metadata_struct.id).await.unwrap();
                if download_result == false {
                    mk_lib_database_download::mk_lib_database_download_insert(db_client,
                                                                              "themoviedb".to_string(),
                                                                              mk_lib_common_enum_media_type::DLMediaType::MOVIE,
                                                                              Uuid::new_v4(),
                                                                              metadata_struct.id,
                                                                              "Fetch".to_string(),
                    ).await;
                }
            }
        }
    }

    // grab the TV id's
    let _fetch_result_tv = mk_lib_networks::mk_download_file_from_url(
        format!("http://files.tmdb.org/p/exports/tv_series_ids_{}.json.gz", fetch_date),
        "tv.gz".to_string());
    let json_result = mk_lib_compression::mk_decompress_gzip("tv.gz").unwrap();
    for json_item in json_result.split('\n') {
        if !json_item.trim().is_empty() {
            let metadata_struct: MetadataTV = serde_json::from_str(json_item)?;
            let result = mk_lib_database_metadata::mk_lib_database_metadata_exists_tv(db_client,
                                                                                      metadata_struct.id).await.unwrap();
            if result == false {
                let download_result = mk_lib_database_download::mk_lib_database_download_exists(db_client,
                                                                                                "themoviedb".to_string(),
                                                                                                mk_lib_common_enum_media_type::DLMediaType::TV,
                                                                                                metadata_struct.id).await.unwrap();
                if download_result == false {
                    mk_lib_database_download::mk_lib_database_download_insert(db_client,
                                                                              "themoviedb".to_string(),
                                                                              mk_lib_common_enum_media_type::DLMediaType::TV,
                                                                              Uuid::new_v4(),
                                                                              metadata_struct.id,
                                                                              "Fetch".to_string(),
                    ).await;
                }
            }
        }
    }

    // stop logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        "bulk_themoviedb_netfetch").await;
    Ok(())
}