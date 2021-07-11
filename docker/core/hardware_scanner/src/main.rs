use amiquip::{AmqpProperties, Connection, Exchange, Publish, Result};
use chrono::prelude::*;
use std::error::Error;
use tokio::time::{Duration, sleep};

#[cfg(debug_assertions)]
#[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
mod mk_lib_logging;

#[cfg(not(debug_assertions))]
#[path = "mk_lib_logging.rs"]
mod mk_lib_logging;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    const LOGGING_INDEX_NAME: &str = "mk_hardware_scanner";
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        LOGGING_INDEX_NAME).await;

//
// media_devices = []
//
    mk_lib_logging::mk_logging_post_elk("info",
                                        "Before Chromcast",
                                        LOGGING_INDEX_NAME).await;
//
// # chromecast discover
// for chromecast_ip, model_name, friendly_name \
//         in common_hardware_chromecast.com_hard_chrome_discover():
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={
//                                                              'chromecast out': chromecast_ip})
//     media_devices.append({'IP': chromecast_ip,
//                           'Model': model_name,
//                           'Name': friendly_name})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After Chromcast",
                                        LOGGING_INDEX_NAME).await;
//
// # dlna devices
// # TODO looks like debugging shows up if run from this program
// # for dlna_devices in common_network_dlna.com_net_dlna_discover():
// #     if dlna_devices.find('No compatible devices found.') != -1:
// #         break
// #     media_devices.append({'DLNA': dlna_devices})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After DLNA",
                                        LOGGING_INDEX_NAME).await;
//
// # hdhomerun tuner discovery
// tuner_api = common_hardware_hdhomerun_py.CommonHardwareHDHomeRunPY()
// tuner_api.com_hdhomerun_discover()
// for row_tuner in tuner_api.com_hdhomerun_list():
//     print(row_tuner, flush=True)
// # tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
// # tuner_api.com_hdhomerun_discover()
// # for row_tuner in tuner_api.com_hdhomerun_list():
// #     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {
// #         'hdhomerun out': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip())})
// #     media_devices.append({'HDHomeRun': {'Model': row_tuner.get_var(item='/sys/model'),
// #                                         'HWModel': row_tuner.get_var(item='/sys/hwmodel'),
// #                                         'Name': row_tuner.get_name(),
// #                                         'ID': str(hex(row_tuner.get_device_id())),
// #                                         'IP': common_string.com_string_ip_int_to_ascii(
// #                                             row_tuner.get_device_ip()),
// #                                         'Firmware': row_tuner.get_version(),
// #                                         'Active': True,
// #                                         'Channels': {}}})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After HDHomerun",
                                        LOGGING_INDEX_NAME).await;
//
// # phillips hue discover
// # TODO this does NOT do discovery
// # hue_inst = common_hardware_hue.CommonHardwareHue()
// # media_devices.append({'Phue': hue_inst.com_hardware_hue_get_api()})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After Phue",
                                        LOGGING_INDEX_NAME).await;
//
// # roku discover
// for roku in common_hardware_roku_network.com_roku_network_discovery():
//     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                          message_text={'roku out': roku})
//     media_devices.append({'Roku': roku})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After Roku",
                                        LOGGING_INDEX_NAME).await;
//
// # soco discover
// soco_devices = common_hardware_soco.com_hardware_soco_discover()
// if soco_devices is not None:
//     for soco in soco_devices:
//         common_logging_elasticsearch_httpx.com_es_httpx_post(
//             message_type='info',
//             message_text={'soco out': soco})
//         media_devices.append({'Soco': soco})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After Soco",
                                        LOGGING_INDEX_NAME).await;
//
// # crestron device discover
// # TODO need to port the script to py3
// # crestron_devices = common_hardware_crestron.com_hardware_crestron_discover()
// # if crestron_devices is not None:
// #     for crestron in crestron_devices:
// #         common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'crestron out': crestron})
// #         media_devices.append({'Crestron': crestron})
    mk_lib_logging::mk_logging_post_elk("info",
                                        "After Crestron",
                                        LOGGING_INDEX_NAME).await;
//
// common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
//                                                      message_text={'devices': media_devices})
//
// common_file.com_file_save_data(file_name='/mediakraken/devices/device_scan.txt',
//                                data_block=media_devices,
//                                as_pickle=True,
//                                with_timestamp=False,
//                                file_ext=None)
}