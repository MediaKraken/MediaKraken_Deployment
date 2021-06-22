use inotify::{
    EventMask,
    Inotify,
    WatchMask,
};
use std::error::Error;

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_library.rs"]
mod mk_lib_database_library;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_library.rs"]
mod mk_lib_database_library;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        "inotify").await;

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    let mut inotify = Inotify::init()
        .expect("Failed to initialize inotify");

    for row_data in mk_lib_database_library::mk_lib_database_library_read(db_client).await.unwrap() {
        inotify.add_watch(
            row_data.get("mm_media_dir_path").to_string(),
            WatchMask::MODIFY | WatchMask::CREATE | WatchMask::DELETE,
        ).expect("Failed to add inotify watch");
    }

    println!("Watching current directory for activity...");

    let mut buffer = [0u8; 4096];
    loop {
        let events = inotify.read_events_blocking(&mut buffer)
            .expect("Failed to read inotify events");
        // process all the events
        for event in events {
            if event.mask.contains(EventMask::CREATE) {
                if event.mask.contains(EventMask::ISDIR) {
                    println!("Directory created: {:?}", event.name);
                } else {
                    println!("File created: {:?}", event.name);
                }
            } else if event.mask.contains(EventMask::DELETE) {
                if event.mask.contains(EventMask::ISDIR) {
                    println!("Directory deleted: {:?}", event.name);
                } else {
                    println!("File deleted: {:?}", event.name);
                }
            } else if event.mask.contains(EventMask::MODIFY) {
                if event.mask.contains(EventMask::ISDIR) {
                    println!("Directory modified: {:?}", event.name);
                } else {
                    println!("File modified: {:?}", event.name);
                }
            }
        }
    }
}