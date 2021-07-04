use amiquip::{AmqpProperties, Connection, Exchange, Publish, Result};
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
    const LOGGING_INDEX_NAME: &str = "mk_file_system_inotify";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    // open rabbit connection
    let mut rabbit_connection = Connection::insecure_open(
        "amqp://guest:guest@mkstack_rabbitmq:5672")?;
    // Open a channel - None says let the library choose the channel ID.
    let rabbit_channel = rabbit_connection.open_channel(None)?;

    // Get a handle to the direct exchange on our channel.
    let rabbit_exchange = Exchange::direct(&rabbit_channel);

    let mut inotify = Inotify::init()
        .expect("Failed to initialize inotify");

    for row_data in mk_lib_database_library::mk_lib_database_library_read(db_client).await.unwrap() {
        let lib_path: String = row_data.get("mm_media_dir_path");
        inotify.add_watch(
            &lib_path,
            WatchMask::MODIFY | WatchMask::CREATE | WatchMask::DELETE,
        ).expect("Failed to add inotify watch");
    }

    let mut buffer = [0u8; 4096];
    loop {
        let events = inotify.read_events_blocking(&mut buffer)
            .expect("Failed to read inotify events");
        // process all the events
        for event in events {
            if event.mask.contains(EventMask::CREATE) {
                if event.mask.contains(EventMask::ISDIR) {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'Dir Create', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("Directory created: {:?}", event.name);
                } else {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'File Create', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("File created: {:?}", event.name);
                }
            } else if event.mask.contains(EventMask::DELETE) {
                if event.mask.contains(EventMask::ISDIR) {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'Dir Delete', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("Directory deleted: {:?}", event.name);
                } else {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'File Delete', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("File deleted: {:?}", event.name);
                }
            } else if event.mask.contains(EventMask::MODIFY) {
                if event.mask.contains(EventMask::ISDIR) {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'Dir Modify', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("Directory modified: {:?}", event.name);
                } else {
                    rabbit_exchange.publish(Publish::with_properties(format!("{{'Type': 'File Modify', 'JSON': {:?}}}", event.name).as_bytes(),
                                                                     "mkinotify".to_string(),
                                                                     AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;
                    println!("File modified: {:?}", event.name);
                }
            }
        }
    }
}