use amiquip::{AmqpProperties, Connection, Exchange, Publish, Result};
use chrono::prelude::*;
use std::error::Error;
use serde_json::{json, Value};
use tokio::time::{Duration, sleep};
use async_std::path::PathBuf;

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
                                        json!({ "Audit Path": str(row_data) }),
                                        LOGGING_INDEX_NAME).await;
        // check for UNC
        let unc_slice= &row_data["mm_media_dir_path"][..1];
        if unc_slice == "\\" {
            addr, share, path = common_string.com_string_unc_to_addr_path(row_data["mm_media_dir_path"]);
            smb_stuff = common_network_cifs.CommonCIFSShare();
            if smb_stuff.com_cifs_open(ip_addr = addr) {
                if smb_stuff.com_cifs_share_directory_check(share, path) {
                    if datetime.strptime(time.ctime(
                        smb_stuff.com_cifs_share_file_dir_info(share, path).last_write_time),
                                         "%a %b %d %H:%M:%S %Y") > row_data["mm_media_dir_last_scanned"] {
                        audit_directories.append((row_data["mm_media_dir_path"],
                                                  row_data["mm_media_dir_class_type"],
                                                  row_data["mm_media_dir_guid"]));
                        db_connection.db_audit_path_update_status(row_data["mm_media_dir_guid"],
                                                                  json.dumps({
                                                                      'Status': 'Added to
                                                                      scan
                                                                      ',
                                                                      'Pct': 100
                                                                  }));
                    }
                } else {
                    mk_lib_database_notification::mk_lib_database_notification_insert(db_client,format!("UNC Library path not found: {}", row_data["mm_media_dir_path"]), true);
                }
            }
        }
        else {
            // make sure the path still exists
            let media_path: PathBuf = ["/mediakraken/mnt",
                row_data["mm_media_dir_path"]].iter().collect();
            if !Path::new(media_path).exists() {
                mk_lib_database_notification::mk_lib_database_notification_insert(db_client,format!("Library path not found: {}", row_data["mm_media_dir_path"]), true);
            }
            else {
                // verify the directory inodes has changed
                if datetime.strptime(
                    time.ctime(os.path.getmtime(
                        media_path)),
                    "%a %b %d %H:%M:%S %Y") > row_data["mm_media_dir_last_scanned"]:
                    audit_directories.append(
                    (media_path,
                     str(row_data["mm_media_class_guid"]),
                     row_data["mm_media_dir_guid"]));
                db_connection.db_audit_path_update_status(row_data["mm_media_dir_guid"],
                                                          json.dumps({
                                                              'Status': 'Added to
                                                              scan
                                                              ',
                                                              'Pct': 100
                                                          }));
            }
        }
    }

// def worker(audit_directory):
//     """
//     Worker thread for each directory
//     """
//     dir_path, media_class_type_uuid, dir_guid = audit_directory
//     # open the database
//     option_config_json, db_connection = common_config_ini.com_config_read()
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={'worker dir': dir_path})
//     original_media_class = media_class_type_uuid
//     # update the timestamp now so any other media added DURING this scan don't get skipped
//     db_connection.db_audit_dir_timestamp_update(dir_path)
//     db_connection.db_audit_path_update_status(dir_guid,
//                                               json.dumps({'Status': 'File search scan',
//                                                           'Pct': 'NA'}))
//     db_connection.db_commit()
//     # check for UNC before grabbing dir list
//     if dir_path[:1] == "\\":
//         file_data = []
//         addr, share, path = common_string.com_string_unc_to_addr_path(dir_path)
//         smb_stuff = common_network_cifs.CommonCIFSShare()
//         smb_stuff.com_cifs_open(addr)
//         for dir_data in smb_stuff.com_cifs_walk(share, path):
//             for file_name in dir_data[2]:
//                 # TODO can I do os.path.join with UNC?
//                 file_data.append('\\\\\'' + addr + '\\' + share + '\\' + dir_data[0]
//                                  + '\\' + file_name + '\'')
//         smb_stuff.com_cifs_close()
//     else:
//         file_data = common_file.com_file_dir_list(dir_path, None, True, False)
//     total_file_in_dir = len(file_data)
//     total_scanned = 0
//     total_files = 0
//     for file_name in file_data:
//         if file_name in global_known_media:
//             pass
//         else:
//             # add to global so next scan won't do again
//             global_known_media.append(file_name)
//             # set lower here so I can remove a lot of .lower() in the code below
//             filename_base, file_extension = os.path.splitext(file_name.lower())
//             # checking subtitles for parts as need multiple files for multiple media files
//             if file_extension[1:] in common_file_extentions.MEDIA_EXTENSION \
//                     or file_extension[1:] in common_file_extentions.SUBTITLE_EXTENSION \
//                     or file_extension[1:] in common_file_extentions.GAME_EXTENSION:
//                 ffprobe_bif_data = True
//                 save_dl_record = True
//                 total_files += 1
//                 # set here which MIGHT be overrode later
//                 new_class_type_uuid = media_class_type_uuid
//                 # check for "stacked" media file
//                 # the split below and the splitext above do return different results
//                 head, base_file_name = os.path.split(file_name)
//                 # check to see if it's a "stacked" file
//                 # including games since some are two or more discs
//                 if common_string.STACK_CD.search(base_file_name) is not None \
//                         or common_string.STACK_PART.search(base_file_name) is not None \
//                         or common_string.STACK_DVD.search(base_file_name) is not None \
//                         or common_string.STACK_PT.search(base_file_name) is not None \
//                         or common_string.STACK_DISK.search(base_file_name) is not None \
//                         or common_string.STACK_DISC.search(base_file_name) is not None:
//                     # check to see if it's part one or not
//                     if common_string.STACK_CD1.search(base_file_name) is None \
//                             and common_string.STACK_PART1.search(base_file_name) is None \
//                             and common_string.STACK_DVD1.search(base_file_name) is None \
//                             and common_string.STACK_PT1.search(base_file_name) is None \
//                             and common_string.STACK_DISK1.search(base_file_name) is None \
//                             and common_string.STACK_DISC1.search(base_file_name) is None:
//                         # it's not a part one here so, no DL record needed
//                         save_dl_record = False
//                 # video game data
//                 # TODO look for cue/bin data as well
//                 if original_media_class == common_global.DLMediaType.Game.value:
//                     if file_extension[1:] == 'iso':
//                         new_class_type_uuid = common_global.DLMediaType.Game_ISO.value
//                     elif file_extension[1:] == 'chd':
//                         new_class_type_uuid = common_global.DLMediaType.Game_CHD.value
//                     else:
//                         new_class_type_uuid = common_global.DLMediaType.Game_ROM.value
//                     ffprobe_bif_data = False
//                 # set new media class for subtitles
//                 elif file_extension[1:] in common_file_extentions.SUBTITLE_EXTENSION:
//                     if original_media_class == common_global.DLMediaType.Movie.value:
//                         new_class_type_uuid = common_global.DLMediaType.Movie_Subtitle.value
//                     elif original_media_class == common_global.DLMediaType.TV.value \
//                             or original_media_class == common_global.DLMediaType.TV_Episode.value \
//                             or original_media_class == common_global.DLMediaType.TV_Season.value:
//                         new_class_type_uuid = common_global.DLMediaType.TV_Subtitle.value
//                     # else:
//                     #     new_class_type_uuid = common_global.DLMediaType.Movie['Subtitle']
//                     ffprobe_bif_data = False
//                 # set new media class for trailers or themes
//                 elif file_name.find('/trailers/') != -1 \
//                         or file_name.find('\\trailers\\') != -1 \
//                         or file_name.find('/theme.mp3') != -1 \
//                         or file_name.find('\\theme.mp3') != -1 \
//                         or file_name.find('/theme.mp4') != -1 \
//                         or file_name.find('\\theme.mp4') != -1:
//                     if original_media_class == common_global.DLMediaType.Movie.value:
//                         if file_name.find('/trailers/') != -1 or file_name.find(
//                                 '\\trailers\\') != -1:
//                             new_class_type_uuid = common_global.DLMediaType.Movie_Trailer.value
//                         else:
//                             new_class_type_uuid = common_global.DLMediaType.Movie_Theme.value
//                     elif original_media_class == common_global.DLMediaType.TV.value \
//                             or original_media_class == common_global.DLMediaType.TV_Episode.value \
//                             or original_media_class == common_global.DLMediaType.TV_Season.value:
//                         if file_name.find('/trailers/') != -1 or file_name.find(
//                                 '\\trailers\\') != -1:
//                             new_class_type_uuid = common_global.DLMediaType.TV_Trailer.value
//                         else:
//                             new_class_type_uuid = common_global.DLMediaType.TV_Theme.value
//                 # set new media class for extras
//                 elif file_name.find('/extras/') != -1 or file_name.find('\\extras\\') != -1:
//                     if original_media_class == common_global.DLMediaType.Movie.value:
//                         new_class_type_uuid = common_global.DLMediaType.Movie_Extras.value
//                     elif original_media_class == common_global.DLMediaType.TV.value \
//                             or original_media_class == common_global.DLMediaType.TV_Episode.value \
//                             or original_media_class == common_global.DLMediaType.TV_Season.value:
//                         new_class_type_uuid = common_global.DLMediaType.TV_Extras.value
//                 # set new media class for backdrops (usually themes)
//                 elif file_name.find('/backdrops/') != -1 \
//                         or file_name.find('\\backdrops\\') != -1:
//                     media_class_text = new_class_type_uuid
//                     if file_name.find('/theme.mp3') != -1 \
//                             or file_name.find('\\theme.mp3') != -1 \
//                             or file_name.find('/theme.mp4') != -1 \
//                             or file_name.find('\\theme.mp4') != -1:
//                         if original_media_class == common_global.DLMediaType.Movie.value:
//                             new_class_type_uuid = common_global.DLMediaType.Movie_Theme.value
//                         elif original_media_class == common_global.DLMediaType.TV.value \
//                                 or original_media_class == common_global.DLMediaType.TV_Episode.value \
//                                 or original_media_class == common_global.DLMediaType.TV_Season.value:
//                             new_class_type_uuid = common_global.DLMediaType.TV_Theme.value
//                 # flip around slashes for smb paths
//                 if file_name[:1] == "\\":
//                     file_name = file_name.replace('\\\\', 'smb://guest:\'\'@').replace('\\', '/')
//                 # create media_json data
//                 media_json = json.dumps({'DateAdded': datetime.now().strftime("%Y-%m-%d")})
//                 media_id = uuid.uuid4()
//                 db_connection.db_insert_media(media_id, file_name, new_class_type_uuid, None, None,
//                                               media_json)
//                 # # verify ffprobe and bif should run on the data
//                 # if ffprobe_bif_data and file_extension[
//                 #                         1:] not in common_file_extentions.MEDIA_EXTENSION_SKIP_FFMPEG \
//                 #         and file_extension[1:] in common_file_extentions.MEDIA_EXTENSION:
//                 #     # Send a message so ffprobe runs
//                 #     channel.basic_publish(exchange='mkque_ffmpeg_ex',
//                 #                           routing_key='mkffmpeg',
//                 #                           body=json.dumps(
//                 #                               {'Type': 'FFProbe', 'Media UUID': str(media_id),
//                 #                                'Media Path': file_name}),
//                 #                           properties=pika.BasicProperties(content_type='text/plain',
//                 #                                                           delivery_mode=2))
//                 #     if original_media_class != common_global.DLMediaType.Music.value:
//                 #         # Send a message so roku thumbnail is generated
//                 #         channel.basic_publish(exchange='mkque_roku_ex',
//                 #                               routing_key='mkroku',
//                 #                               body=json.dumps(
//                 #                                   {'Type': 'Roku', 'Subtype': 'Thumbnail',
//                 #                                    'Media UUID': str(media_id),
//                 #                                    'Media Path': file_name}),
//                 #                               properties=pika.BasicProperties(
//                 #                                   content_type='text/plain',
//                 #                                   delivery_mode=2))
//                 # verify it should save a dl "Z" record for search/lookup/etc
//                 if save_dl_record:
//                     # media id begin and download que insert
//                     db_connection.db_download_insert(provider='Z',
//                                                      que_type=new_class_type_uuid,
//                                                      down_json=json.dumps({'MediaID': str(media_id),
//                                                                            'Path': file_name}),
//                                                      down_new_uuid=uuid.uuid4(),
//                                                      )
//         total_scanned += 1
//         db_connection.db_audit_path_update_status(dir_guid,
//                                                   json.dumps({'Status': 'File scan: '
//                                                                         + common_internationalization.com_inter_number_format(
//                                                       total_scanned)
//                                                                         + ' / ' + common_internationalization.com_inter_number_format(
//                                                       total_file_in_dir),
//                                                               'Pct': (
//                                                                              total_scanned / total_file_in_dir) * 100}))
//         db_connection.db_commit()
//     # end of for loop for each file in library
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={'worker dir done': dir_path,
//                                                                        'media class': media_class_type_uuid})
//     # set to none so it doesn't show up anymore in admin status page
//     db_connection.db_audit_path_update_status(dir_guid, None)
//     if total_files > 0:
//         # add notification to admin status page
//         db_connection.db_notification_insert(
//             common_internationalization.com_inter_number_format(total_files)
//             + " file(s) added from " + dir_path, True)
//     db_connection.db_commit()
//     db_connection.db_close()
//     return

    // commit
    db_connection.db_commit();

    // Cancel the consumer and return any pending messages
    channel.cancel();

    // close pika
    channel.close(); // throws error as previously closed

    // close the database
    db_connection.db_close();

    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
}