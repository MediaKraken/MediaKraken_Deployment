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
#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_cron.rs"]
mod mk_lib_database_cron;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database.rs"]
mod mk_lib_database;
#[cfg(not(debug_assertions))]
#[path = "mk_lib_database_cron.rs"]
mod mk_lib_database_cron;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "mk_schedules_direct_update";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

//
// def mk_schedules_direct_program_info_fetch(meta_program_fetch):
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={'array': meta_program_fetch})
//     meta_program_json = sd.com_schedules_direct_program_info(
//         json.dumps(meta_program_fetch))
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={'result': meta_program_json})
//     #   meta_program_json = sd.com_Schedules_Direct_Program_Desc(
//     # json.dumps([{'programID': program_json['programID']}]))
//     for program_data in meta_program_json:
//         db_connection.db_tv_program_insert(
//             program_json['programID'], json.dumps(program_data))
//
//
// sd = common_schedules_direct.CommonSchedulesDirect()
// sd.com_schedules_direct_login(option_config_json['SD']['User'],
//                               option_config_json['SD']['Password'])
// status_data = sd.com_schedules_direct_status()
// if status_data['systemStatus'][0]['status'] == "Online":
//     pass
// else:
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='critical',
//                                                          message_text={'stuff': 'SD is unavailable'})
//     sys.exit(0)
// # version check
// # version_json = sd.com_Schedules_Direct_Client_Version()
// # TODO
// # if version_json != "MediaKraken_0.1.0":
// #    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='critical', message_text= {'stuff':"Outdated Client Version! Upgrade MediaKraken_")
// #    sys.exit(0)
//
// # get headends
// # headends_json = sd.com_Schedules_Direct_Headends('USA', '58701')
//
// # add to lineup
// # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':sd.com_Schedules_Direct_Lineup_Add('USA-ND33420-DEFAULT'))
//
// # remove from lineup
// # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':sd.com_Schedules_Direct_Lineup_Delete('USA-DISH687-DEFAULT'))
//
//
// # list lineups and channels for them
// # for line_name in sd.com_Schedules_Direct_Lineup_List()['lineups']:
// #    # channel map
// #    channel_map = sd.com_Schedules_Direct_Lineup_Channel_Map(line_name['lineup'])
// #    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':"Map: %s", channel_map['map'])
// #    for channel_id in channel_map['map']:
// #        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':"mapchannel: %s", channel_id)
// #        db_connection.db_tv_station_insert(channel_id['stationID'], channel_id['channel'])
// #    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':"Stations: %s", channel_map['stations'])
// #    for channel_meta in channel_map['stations']:
// #        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff':"stationschannel: %s", channel_meta)
// #        db_connection.db_tv_station_update(channel_meta['name'], channel_meta['stationID'],\
// # json.dumps(channel_meta))
//
//
// # TODO downloading a generic description of a program
// # - good for what the show is......not an episode itself
//
// station_fetch = []
// common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
//     'list': db_connection.db_tv_stations_read_stationid_list()})
// # grab all stations in DB
// for station_id in db_connection.db_tv_stations_read_stationid_list():
//     # fetch all schedules for station
//     station_fetch.append(station_id['mm_tv_station_id'])
//
// # set here so it exists at the "end" of processing
// meta_program_fetch = []
// # grab station info from SD
// if len(station_fetch) > 5000:
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='critical', message_text=
//                                             {'stuff': 'Too many channels!!!!  Exiting...'})
// elif len(station_fetch) > 0:
//     schedule_json = sd.com_schedules_direct_schedules_by_stationid(
//         json.dumps(station_fetch))
//     # for each station in schedules results
//     for station_json in schedule_json:
//         # [{u'stationID': u'10093', u'metadata': {u'startDate': u'2016-06-15',
//         # u'modified': u'2016-06-14T23:07:05Z', u'md5': u'2aEwFuhZCqJSHKabBbR/Sg'},
//         meta_program_fetch = []
//         # for each program in station schedule result
//         for program_json in station_json['programs']:
//             # {u'ratings': [{u'body': u'USA Parental Rating', u'code': u'TV14'}],
//             # u'audioProperties': [u'DD 5.1', u'stereo'], u'duration': 9000,
//             # u'programID': u'MV000135600000', u'airDateTime': u'2016-06-15T00:30:00Z',
//             #  u'md5': u'18/KxBZUiJQu5sCix7WWwQ'},
//             db_connection.db_tv_schedule_insert(station_json['stationID'],
//                                                 program_json['airDateTime'],
//                                                 json.dumps(program_json))
//             common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
//             {'programid': program_json['programID']})
//             # if program_json['programID'][0:2] != "MV":
//             meta_program_fetch.append(program_json['programID'])
//             if len(meta_program_fetch) >= 500:
//                 mk_schedules_direct_program_info_fetch(meta_program_fetch)
//                 meta_program_fetch = []
//
// # TODO check to see if meta array has unstored data
// if len(meta_program_fetch) > 0:
//     mk_schedules_direct_program_info_fetch(meta_program_fetch)
//
// # TODO, go grab images for blank logos
}