use serde::{Deserialize, Serialize};
use std::error::Error;
use uuid::Uuid;

mod mk_lib_database_metadata;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_network;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_network.rs"]
mod mk_lib_network;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "libretro_core_netfetch";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

    // populate current cores
    let libretro_current_core = common_file.com_file_dir_list("/mediakraken/emulation/cores",
                                                          filter_text=None, walk_dir=None,
                                                          skip_junk=False, file_size=False,
                                                          directory_only=False,
                                                          file_modified=True);

    let libtro_url = "http://buildbot.libretro.com/nightly/linux/x86_64/latest/";
    // date md5 core_filename.zip
    for libretro_core in common_network.mk_network_fetch_from_url(libtro_url
                                                                  + ".index-extended").split("\n") {
        download_core = false;
        core_date, core_md5, core_name = libretro_core.split(" ");
        if core_name in libretro_current_core {
            // we have the core, check to see if it's newer
            if libretro_current_core[core_name] < core_date.replace("-", "") {
                download_core = true;
            }
        }
        else
        {
        download_core = true;
        }
        if download_core {
            // download the missing or newer core
            common_network.mk_network_fetch_from_url(libtro_url + core_name,
                                                     "/mediakraken/emulation/cores/" + core_name);
            // unzip the core for use
            common_file.com_file_unzip("/mediakraken/emulation/cores/" + core_name,
                                       target_destination_directory = None, remove_zip = true);
        }
    }

    // stop logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
    Ok(())
}