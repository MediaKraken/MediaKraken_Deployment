use amiquip::{AmqpProperties, Connection, Exchange, Publish, Result};
use chrono::prelude::*;
use std::error::Error;
use tokio::time::{Duration, sleep};

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database.rs"]
mod mk_lib_database;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "mk_metadata_tmdb";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;


    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
}