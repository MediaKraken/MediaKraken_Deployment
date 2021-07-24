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
mod mk_lib_network;

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
mod mk_lib_network;

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
    const LOGGING_INDEX_NAME: &str = "mk_tmdb_netfetch_update";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    // option_config_json, db_connection = \
    //     await common_config_ini.com_config_read_async(loop=loop,
    //                                                   as_pool=False)
    //
    // # TODO this should go through the limiter
    // # process movie changes
    // new_movie_data = json.loads(await common_network_async.mk_network_fetch_from_url_async(
    //     'https://api.themoviedb.org/3/movie/changes'
    //     '?api_key=%s' % option_config_json['API']['themoviedb']))
    // for movie_change in new_movie_data['results']:
    //     await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
    //                                                                      message_text={
    //                                                                          'mov': movie_change[
    //                                                                              'id']})
    //     # verify it's not already in the database
    //     if (await db_connection.db_meta_movie_count_by_id(guid=movie_change['id'],
    //                                                       db_connection=None) is False
    //             and await db_connection.db_download_que_exists(download_que_uuid=None,
    //                                                            download_que_type=common_global.DLMediaType.Movie.value,
    //                                                            provider_name='themoviedb',
    //                                                            provider_id=movie_change['id'],
    //                                                            db_connection=None,
    //                                                            exists_only=True) is False):
    //         await db_connection.db_download_insert(provider='themoviedb',
    //                                                que_type=common_global.DLMediaType.Movie.value,
    //                                                down_json={'Status': 'Fetch',
    //                                                           'ProviderMetaID':
    //                                                               movie_change['id']},
    //                                                down_new_uuid=uuid.uuid4(),
    //                                                db_connection=None
    //                                                )
    //     else:
    //         # it's on the database, so must update the record with latest information
    //         await db_connection.db_download_insert(provider='themoviedb',
    //                                                que_type=common_global.DLMediaType.Movie.value,
    //                                                down_json={'Status': 'Update',
    //                                                           'ProviderMetaID':
    //                                                               movie_change['id']},
    //                                                down_new_uuid=uuid.uuid4(),
    //                                                db_connection=None
    //                                                )
    //
    // # TODO this should go through the limiter
    // # process tv changes
    // new_tv_data = json.loads(await common_network_async.mk_network_fetch_from_url_async(
    //     'https://api.themoviedb.org/3/tv/changes'
    //     '?api_key=%s' % option_config_json['API']['themoviedb']))
    // for tv_change in new_tv_data['results']:
    //     await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
    //                                                                      message_text={
    //                                                                          'stuff': "tv: %s" %
    //                                                                                   tv_change[
    //                                                                                       'id']})
    //     # verify it's not already in the database
    //     if (await db_connection.db_meta_tv_count_by_id(guid=tv_change['id'],
    //                                                    db_connection=None) is False
    //             and await db_connection.db_download_que_exists(download_que_uuid=None,
    //                                                            download_que_type=common_global.DLMediaType.TV.value,
    //                                                            provider_name='themoviedb',
    //                                                            provider_id=tv_change['id'],
    //                                                            db_connection=None,
    //                                                            exists_only=True) is False):
    //         await db_connection.db_download_insert(provider='themoviedb',
    //                                                que_type=common_global.DLMediaType.TV.value,
    //                                                down_json={'Status': 'Fetch',
    //                                                           'ProviderMetaID':
    //                                                               tv_change['id']},
    //                                                down_new_uuid=uuid.uuid4(),
    //                                                db_connection=None
    //                                                )
    //     else:
    //         # it's on the database, so must update the record with latest information
    //         await db_connection.db_download_insert(provider='themoviedb',
    //                                                que_type=common_global.DLMediaType.TV.value,
    //                                                down_json={'Status': 'Update',
    //                                                           'ProviderMetaID':
    //                                                               tv_change['id']},
    //                                                down_new_uuid=uuid.uuid4(),
    //                                                db_connection=None
    //                                                )
    //
    // # commit all changes
    // await db_connection.db_commit(db_connection=None)
    //
    // # close DB
    // await db_connection.db_close(db_connection=None)
    //



    // stop logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "STOP",
                                        LOGGING_INDEX_NAME).await;
    Ok(())
}