use amiquip::{AmqpProperties, Connection, Exchange, Publish, Result};
use async_std::path::PathBuf;
use chrono::prelude::*;
use num_format::{Locale, ToFormattedString};
use serde_json::{json, Value};
use std::error::Error;
use std::path::Path;
use tokio::time::{Duration, sleep};

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_file/src/mk_lib_file.rs"]
mod mk_lib_file;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_library.rs"]
mod mk_lib_database_library;
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_notification.rs"]
mod mk_lib_database_notification;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_file.rs"]
mod mk_lib_file;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_library.rs"]
mod mk_lib_database_library;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_notification.rs"]
mod mk_lib_database_notification;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "mk_file_system_media_scanner";
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

    // determine directories to audit
    for row_data in mk_lib_database_library::mk_lib_database_library_path_audit(db_client).await.unwrap() {
        mk_lib_logging::mk_logging_post_elk("info",
                                            json!({ "Audit Path": row_data }),
                                            LOGGING_INDEX_NAME).await;
        // check for UNC
        let unc_slice = &row_data["mm_media_dir_path"][..1];
        if unc_slice == "\\" {
            continue;
            // addr, share, path = common_string.com_string_unc_to_addr_path(row_data["mm_media_dir_path"]);
            // smb_stuff = common_network_cifs.CommonCIFSShare();
            // if smb_stuff.com_cifs_open(ip_addr = addr) {
            //     if smb_stuff.com_cifs_share_directory_check(share, path) {
            //         if datetime.strptime(time.ctime(
            //             smb_stuff.com_cifs_share_file_dir_info(share, path).last_write_time),
            //                              "%a %b %d %H:%M:%S %Y") > row_data["mm_media_dir_last_scanned"] {
            //             audit_directories.append((row_data["mm_media_dir_path"],
            //                                       row_data["mm_media_dir_class_type"],
            //                                       row_data["mm_media_dir_guid"]));
            //             db_connection.db_audit_path_update_status(row_data["mm_media_dir_guid"],
            //                                                       json.dumps({
            //                                                           "Status": "Added to
            //                                                           scan
            //                                                           ",
            //                                                           "Pct": 100
            //                                                       }));
            //         }
            //     } else {
            //         mk_lib_database_notification::mk_lib_database_notification_insert(db_client,format!("UNC Library path not found: {}", row_data["mm_media_dir_path"]), true);
            //     }
            // }
        } else {
            // make sure the path still exists
            let media_path: PathBuf = ["/mediakraken/mnt",
                row_data["mm_media_dir_path"]].iter().collect();
            if !Path::new(&media_path).exists() {
                mk_lib_database_notification::mk_lib_database_notification_insert(db_client,
                                                                                  format!("Library path not found: {}",
                                                                                          row_data["mm_media_dir_path"]),
                                                                                  true).await.unwrap();
            } else {
                // verify the directory inodes has changed
                let metadata = fs::metadata(&media_path)?;
                let last_modified = metadata.modified()?.elapsed()?.as_secs();
                if last_modified > row_data["mm_media_dir_last_scanned"] {
                    mk_lib_database_library::mk_lib_database_library_path_status_update(db_client,
                                                                                        row_data["mm_media_dir_guid"],
                                                                                        json!({"Status": "Added to scan", "Pct": 100})).await.unwrap();

                    mk_lib_logging::mk_logging_post_elk("info",
                                                        json!({"worker dir": dir_path}),
                                                        LOGGING_INDEX_NAME).await;

                    original_media_class = media_class_type_uuid;
                    // update the timestamp now so any other media added DURING this scan don"t get skipped
                    mk_lib_database_library::mk_lib_database_library_path_timestamp_update(db_client,
                                                                                           row_data["mm_media_dir_guid"]).await.unwrap();
                    mk_lib_database_library::mk_lib_database_library_path_status_update(db_client,
                                                                                        row_data["mm_media_dir_guid"],
                                                                                        json!({"Status": "File search scan", "Pct": 0.0})).await.unwrap();

                    // check for UNC before grabbing dir list
                    if unc_slice == "\\" {
                        file_data = [];
                        addr, share, path = common_string.com_string_unc_to_addr_path(dir_path);
                        smb_stuff = common_network_cifs.CommonCIFSShare();
                        smb_stuff.com_cifs_open(addr);
                        for dir_data in smb_stuff.com_cifs_walk(share, path) {
                            for file_name in dir_data[2] {
                                // TODO can I do os.path.join with UNC?
                                file_data.append("\\\\\"" + addr + "\\" + share + "\\" + dir_data[0] + "\\" + file_name + "\"");
                            }
                        }
                        smb_stuff.com_cifs_close();
                    } else {
                        file_data = mk_lib_file::mk_directory_walk(&dir_path);
                    }
                    total_file_in_dir = len(file_data);
                    total_scanned = 0;
                    total_files = 0;
                    for file_name in file_data {
                        if mk_lib_database_library::mk_lib_database_library_file_exists(db_client,
                                                                                        &file_name).await.unwrap() == false {
                            // set lower here so I can remove a lot of .lower() in the code below
                            let file_extension = Path::new(&file_name).extension().to_lowercase();

                            // checking subtitles for parts as need multiple files for multiple media files
                                         if file_extension in common_file_extentions.MEDIA_EXTENSION \
                                                 || file_extension in common_file_extentions.SUBTITLE_EXTENSION \
                                                 || file_extension in common_file_extentions.GAME_EXTENSION:
                                             ffprobe_bif_data = true;
                                             save_dl_record = true;
                                             total_files += 1;
                            // set here which MIGHT be overrode later
                                             new_class_type_uuid = media_class_type_uuid;
                            // check for "stacked" media file
                            // the split below and the splitext above do return different results
                                             head, base_file_name = os.path.split(file_name);
                            // check to see if it"s a "stacked" file
                            // including games since some are two or more discs
                                             if common_string.STACK_CD.search(base_file_name) is not None \
                                                     || common_string.STACK_PART.search(base_file_name) is not None \
                                                     || common_string.STACK_DVD.search(base_file_name) is not None \
                                                     || common_string.STACK_PT.search(base_file_name) is not None \
                                                     || common_string.STACK_DISK.search(base_file_name) is not None \
                                                     || common_string.STACK_DISC.search(base_file_name) is not None:
                            // check to see if it"s part one or not
                                                 if common_string.STACK_CD1.search(base_file_name) is None \
                                                         && common_string.STACK_PART1.search(base_file_name) is None \
                                                         && common_string.STACK_DVD1.search(base_file_name) is None \
                                                         && common_string.STACK_PT1.search(base_file_name) is None \
                                                         && common_string.STACK_DISK1.search(base_file_name) is None \
                                                         && common_string.STACK_DISC1.search(base_file_name) is None:
                                                     // it"s not a part one here so, no DL record needed
                                                     save_dl_record = false;
                                             // video game data
                                             // TODO look for cue/bin data as well
                                             if original_media_class == common_global.DLMediaType.Game.value {
                                                 if file_extension == "iso" {
                                                     new_class_type_uuid = common_global.DLMediaType.Game_ISO.value;
                            }
                                                 else if file_extension == "chd" {
                                                     new_class_type_uuid = common_global.DLMediaType.Game_CHD.value;
                             }
                                                 else {
                                                     new_class_type_uuid = common_global.DLMediaType.Game_ROM.value;
                            }
                                                 ffprobe_bif_data = false;
                            }
                            //                 // set new media class for subtitles
                                             else if file_extension in common_file_extentions.SUBTITLE_EXTENSION:
                                                 if original_media_class == common_global.DLMediaType.Movie.value {
                                                     new_class_type_uuid = common_global.DLMediaType.Movie_Subtitle.value;
                            }
                                                 elif original_media_class == common_global.DLMediaType.TV.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Episode.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Season.value {
                                                     new_class_type_uuid = common_global.DLMediaType.TV_Subtitle.value;
                            }
                            //                     # else:
                            //                     #     new_class_type_uuid = common_global.DLMediaType.Movie["Subtitle"]
                                                 ffprobe_bif_data = false;
                                             // set new media class for trailers or themes
                                             else if file_name.find("/trailers/") != -1 \
                                                     || file_name.find("\\trailers\\") != -1 \
                                                     || file_name.find("/theme.mp3") != -1 \
                                                     || file_name.find("\\theme.mp3") != -1 \
                                                     || file_name.find("/theme.mp4") != -1 \
                                                     || file_name.find("\\theme.mp4") != -1:
                                                 if original_media_class == common_global.DLMediaType.Movie.value {
                                                     if file_name.find("/trailers/") != -1 || file_name.find(
                                                             "\\trailers\\") != -1 {
                                                         new_class_type_uuid = common_global.DLMediaType.Movie_Trailer.value;
                            }
                                                     else {
                                                         new_class_type_uuid = common_global.DLMediaType.Movie_Theme.value;
                            }
                            }
                                                 elif original_media_class == common_global.DLMediaType.TV.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Episode.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Season.value {
                                                     if file_name.find("/trailers/") != -1 || file_name.find(
                                                             "\\trailers\\") != -1 {
                                                         new_class_type_uuid = common_global.DLMediaType.TV_Trailer.value;
                            }
                                                     else {
                                                         new_class_type_uuid = common_global.DLMediaType.TV_Theme.value;
                            }
                            }
                                             // set new media class for extras
                                             else if file_name.find("/extras/") != -1 || file_name.find("\\extras\\") != -1:
                                                 if original_media_class == common_global.DLMediaType.Movie.value {
                                                     new_class_type_uuid = common_global.DLMediaType.Movie_Extras.value;
                            }
                                                 elif original_media_class == common_global.DLMediaType.TV.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Episode.value \
                                                         || original_media_class == common_global.DLMediaType.TV_Season.value {
                                                     new_class_type_uuid = common_global.DLMediaType.TV_Extras.value;
                            }
                                             // set new media class for backdrops (usually themes)
                                             else if file_name.find("/backdrops/") != -1 \
                                                     || file_name.find("\\backdrops\\") != -1
                            {
                                media_class_text = new_class_type_uuid;
                            }
                                                 if file_name.find("/theme.mp3") != -1 \
                                                         || file_name.find("\\theme.mp3") != -1 \
                                                         || file_name.find("/theme.mp4") != -1 \
                                                         || file_name.find("\\theme.mp4") != -1
                            {
                                if original_media_class == common_global.DLMediaType.Movie.value {
                                    new_class_type_uuid = common_global.DLMediaType.Movie_Theme.value;
                                } else if original_media_class == common_global.DLMediaType.TV.value \
                                || original_media_class == common_global.DLMediaType.TV_Episode.value \
                                || original_media_class == common_global.DLMediaType.TV_Season.value:
                                    new_class_type_uuid = common_global.DLMediaType.TV_Theme.value;
                            }
                                             // flip around slashes for smb paths
                                             if file_name == "\\" {
                                                 file_name = file_name.replace("\\\\", "smb://guest:\"\"@").replace("\\", "/");
                            }
                                             // create media_json data
                                             media_json = json.dumps({"DateAdded": datetime.now().strftime("%Y-%m-%d")});
                                             media_id = uuid.uuid4();
                                             db_connection.db_insert_media(media_id, file_name, new_class_type_uuid, None, None,
                                                                           media_json);
                                             // verify ffprobe and bif should run on the data
                                              if ffprobe_bif_data && file_extension not in common_file_extentions.MEDIA_EXTENSION_SKIP_FFMPEG \
                                                      && file_extension in common_file_extentions.MEDIA_EXTENSION
                            {
                                // Send a message so ffprobe runs
                                channel.basic_publish(exchange = "mkque_ffmpeg_ex",
                                                      routing_key = "mkffmpeg",
                                                      body = json.dumps(
                                                          {
                                                              "Type": "FFProbe", "Media UUID": str(media_id),
                                                              "Media Path": file_name
                                                          }),
                                                      properties = pika.BasicProperties(content_type = "text/plain",
                                                                                        delivery_mode = 2));
                                if original_media_class != common_global.DLMediaType.Music.value {
                                    // Send a message so roku thumbnail is generated
                                    channel.basic_publish(exchange = "mkque_roku_ex",
                                                          routing_key = "mkroku",
                                                          body = json.dumps(
                                                              {
                                                                  "Type": "Roku", "Subtype": "Thumbnail",
                                                                  "Media UUID": str(media_id),
                                                                  "Media Path": file_name
                                                              }),
                                                          properties = pika.BasicProperties(
                                                              content_type = "text/plain",
                                                              delivery_mode = 2));
                                }
                            }
                                             // verify it should save a dl "Z" record for search/lookup/etc
                                             if save_dl_record {
                                                 // media id begin and download que insert
                                                 db_connection.db_download_insert(provider="Z",
                                                                                  que_type=new_class_type_uuid,
                                                                                  down_json=json.dumps({"MediaID": str(media_id),
                                                                                                        "Path": file_name}),
                                                                                  down_new_uuid=uuid.uuid4(),
                                                                                  );
                             }
                            }
                                     total_scanned += 1;
                                     mk_lib_database_library::mk_lib_database_library_path_status_update(db_client,
                                                                                                         row_data["mm_media_dir_guid"],
                                                                               json!({"Status": "File scan: " + total_scanned.to_formatted_string(&Locale::en)
                                                                                                     + "/" + total_file_in_dir.to_formatted_string(&Locale::en),
                                                                                           "Pct": (total_scanned / total_file_in_dir) * 100}));

                        }
                    }
                    // end of for loop for each file in library
                    mk_lib_logging::mk_logging_post_elk("info",
                                                        json!({"worker dir done": dir_path,
                                            "media class": media_class_type_uuid}),
                                                        LOGGING_INDEX_NAME).await;
                    // set to none so it doesn"t show up anymore in admin status page
                    mk_lib_database_library::mk_lib_database_library_path_status_update(db_client,
                                                                                        row_data["mm_media_dir_guid"],
                                                                                        json!({"Status": "File scan complete", "Pct": 100}));
                    if total_files > 0 {
                        // add notification to admin status page
                        mk_lib_database_notification::mk_lib_database_notification_insert(db_client,
                                                                                          format!("{} file(s) added from {}",
                                                                                                  total_files.to_formatted_string(&Locale::en),
                                                                                                  row_data["mm_media_dir_path"]), true);
                    }
                }
            }
        }
    }

    // close rabbitmq
    rabbit_connection.close();

    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
    Ok(())
}