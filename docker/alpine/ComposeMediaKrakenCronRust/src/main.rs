use amiquip::{Connection, Exchange, Publish, Result};
use chrono::prelude::*;
use std::env;
//use std::error::Error;
use tokio::time::{Duration, sleep};
//use tokio_postgres::{Error};

// #[path = "../../../../source_rust/mk_lib_logging/src/mk_lib_logging.rs"]
// mod mk_lib_logging;
#[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database.rs"]
mod mk_lib_database;
// #[path = "../../../../source_rust/mk_lib_database/src/mk_lib_database_cron.rs"]
// mod mk_lib_database_cron;
#[path = "../../../../source_rust/mk_lib_network/src/mk_lib_network.rs"]
mod mk_lib_network;

#[tokio::main]
async fn main() -> Result<()> {
    // start logging
    // mk_lib_logging::mk_logging_post_elk("info",
    //                                     "START",
    //                                     "cron_checker");
    // open the database
    let dp_pass = env::var("POSTGRES_PASSWORD").unwrap();
    let db_client = mk_lib_database::mk_lib_database_open(&dp_pass);

    // fire off wait for it script to verify rabbitmq is available
    // mk_lib_network::mk_network_service_available("mkstack_rabbitmq",
    //                                              "5672", "120");

    // // open rabbit connection
    // let mut rabbit_connection = Connection::insecure_open(
    //     "amqp://guest:guest@mkstack_rabbitmq:5672")?;
    // // Open a channel - None says let the library choose the channel ID.
    // let rabbit_channel = rabbit_connection.open_channel(None)?;
    //
    // // // Declare the fanout exchange we will bind to.
    // // let exchange = rabbit_channel.exchange_declare(
    // //     ExchangeType::Direct,
    // //     "direct_logs",
    // //     ExchangeDeclareOptions::default(),
    // // )?;
    //
    // // Get a handle to the direct exchange on our channel.
    // let rabbit_exchange = Exchange::direct(&rabbit_channel);
    //
    // // start loop for cron checks
    // loop {
    //     for row_data in mk_lib_database_cron::mk_lib_database_cron_service_read(db_client) {
    //         let mut time_delta;
    //         if row_data.get("mm_cron_schedule") == "Weekly" {
    //             time_delta = chrono::Duration::weeks(1);
    //         } else {
    //             let time_span_vector: Vec<&str>
    //                 = row_data.get("mm_cron_schedule").split(' ').collect();
    //             if time_span_vector[0] == "Days" {
    //                 time_delta = chrono::Duration::days(time_span_vector[1].parse().unwrap());
    //             } else if time_span_vector[0] == "Hours" {
    //                 time_delta = chrono::Duration::hours(time_span_vector[1].parse().unwrap());
    //             } else {
    //                 // time_span_vector[0] == "Minutes":
    //                 time_delta = chrono::Duration::minutes(time_span_vector[1].parse().unwrap());
    //             }
    //         }
    //         let utc: DateTime<Utc> = Utc::now();
    //         let date_check = utc - time_delta;
    //         if row_data.get("mm_cron_last_run") < date_check {
    //             let cron_json = row_data.try_get::<&str, serde_json::Value>("mm_cron_json")?;
    //             rabbit_exchange.publish(Publish::new("hello there".as_bytes(),
    //                                                  cron_json["exchange_key"]))?;
    //             // channel.basic_publish(exchange = row_data.get("mm_cron_json")("exchange_key"),
    //             //                       routing_key = row_data['mm_cron_json']['route_key'],
    //             //                       body = json.dumps(
    //             //                           {
    //             //                               'Type': row_data['mm_cron_json']['Type'],
    //             //                               'JSON': row_data['mm_cron_json']
    //             //                           }),
    //             //                       properties = pika.BasicProperties(
    //             //                           content_type ='text/plain',
    //             //                           delivery_mode = 2),
    //             //)
    //         }
    //         // db_client.mk_lib_database_cron_time_update(row_data.get("mm_cron_guid"));
    //         // db_client.commit().await.unwrap();
    //         // mk_lib_logging::mk_logging_post_elk("info",
    //         //                                     row_data,
    //         //                                     "cron_checker");
    //     }
    //     sleep(Duration::from_secs(60)).await;
    // }
    // Code below can't be hit currently. So, drop the commands.
    // close the rabbit connection
    // rabbit_connection.close();
    // close the database
    // db_client.db_close();
}