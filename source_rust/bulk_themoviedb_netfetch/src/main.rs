// launch the vs tools app otherwise can't compile (windows os only)

use std::error::Error;
// use postgres::{Client, Error, NoTls};
// use serde_json::{Result, Value};

#[path = "../../lib_common/mk_lib_common.rs"] mod mk_lib_common;
#[path = "../../lib_compression/mk_lib_compression.rs"] mod mk_lib_compression;
#[path = "../../lib_database/mk_lib_database.rs"] mod mk_lib_database;
#[path = "../../lib_network/mk_lib_network.rs"] mod mk_lib_networks;

fn main() -> Result<(), Box<dyn Error>> {
    let fetch_date: String = "05_15_2021".to_string();

    // grab the movie id's
    // let fetch_result = mk_lib_networks::mk_download_file_from_url(
    //     &format!("http://files.tmdb.org/p/exports/movie_ids_{}.json.gz", fetch_date),
    //     "movie.gz");
    let json_result = mk_lib_compression::mk_decompress_gzip("movie.gz").unwrap();
    // match json_result {
    //         Ok(value) => {
    //             println!("jsondata: {:?}", value);
    //             // Parse the string of data into serde_json::Value.
    //             let v: serde_json::Value = serde_json::from_str(&value);
    //         },
    //         Err(error) => {
    //             println!("{}", error);
    //         },
    //     }
    println!("jsondata: {:?}", json_result);
    // Parse the string of data into serde_json::Value.
    let v: serde_json::Value = serde_json::from_str(json_result);
    //println!("Please call {} at the number {}", v["id"], v["adult"]);

    // // grab the TV id's
    // let fetch_result = mk_lib_networks::mk_download_file_from_url(
    //     &format!("http://files.tmdb.org/p/exports/tv_series_ids_{}.json.gz", fetch_date),
    //     "tv.gz");
    // let json_data = mk_lib_compression::mk_decompress_gzip("tv.gz");
    //
    // // connect to postgresql
    // let mut client = Client::connect("postgresql://postgres:metaman@localhost/postgres", NoTls)?;
    //
    // // let row = client.query_one("SELECT foo FROM bar WHERE baz = $1", &[&baz])?;
    // // let foo: i32 = row.get("foo");
    // // println!("foo: {}", foo);
    //
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
    //
    //     println!("found person: {} {} {:?}", id, name, data);
    // }
    Ok(())
}