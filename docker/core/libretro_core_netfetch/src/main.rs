use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::error::Error;
use std::fs;

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_compression/src/mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_hash/src/mk_lib_hash_md5.rs"]
mod mk_lib_hash_md5;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_network;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_compression.rs"]
mod mk_lib_compression;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_hash_md5.rs"]
mod mk_lib_hash_md5;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_network.rs"]
mod mk_lib_network;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "mk_libretro_core_netfetch";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

    // populate current cores into hashmap
    let mut emulation_cores = HashMap::new();
    let walker = WalkDir::new("/mediakraken/emulation/cores").into_iter();
    for entry in walker.filter_entry(|e| !is_hidden(e)) {
        let entry = entry.unwrap();
        emulation_cores.insert(entry.path().display().split(".")[0],
                               mk_lib_hash_md5::mk_file_hash_md5(
                                   entry.path().display()));
    }

    // date md5 core_filename.zip
    let libtro_url = "http://buildbot.libretro.com/nightly/linux/x86_64/latest/";
    let fetch_result = mk_lib_network::mk_data_from_url(
        libtro_url + ".index-extended").await;
    for libretro_core in fetch_result.split('\n') {
        let mut download_core = false;
        let (core_date, core_md5, core_name) = libretro_core.split(" ");
        if emulation_cores.contains_key(core_name) {
            // we have the core, check to see if md5 changed
            if emulation_cores[core_name][1] != core_md5 {
                download_core = true;
            }
        } else {
            download_core = true;
        }
        if download_core {
            // download the missing or newer core
            mk_lib_network::mk_download_file_from_url(libtro_url + core_name,
                                                      "/mediakraken/emulation/cores/"
                                                          + core_name);
            // unzip the core for use
            mk_lib_compression::mk_decompress_zip("/mediakraken/emulation/cores/"
                                                      + core_name,
                                                  true,
                                                  true);
        }
    }

    // stop logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
    Ok(())
}