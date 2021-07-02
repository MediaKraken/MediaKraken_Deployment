#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_compression/src/mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_network;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_network.rs"]
mod mk_lib_network;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let fetch_date: String = "06_20_2021".to_string();

    // grab the movie id's
    // files.tmdb.org = 13.227.42.62
    let _fetch_result_movie = mk_lib_network::mk_download_file_from_url(
        format!("http://files.tmdb.org/p/exports/movie_ids_{}.json.gz", fetch_date),
        "/myapp/movie.gz".to_string()).await;
    let json_result = mk_lib_compression::mk_decompress_gzip("/myapp/movie.gz").unwrap();
    Ok(())
}