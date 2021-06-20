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
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        "cron_checker").await;

    // open the database
    let db_client = &mk_lib_database::mk_lib_database_open().await?;

    // open rabbit connection
    let mut rabbit_connection = Connection::insecure_open(
        "amqp://guest:guest@mkstack_rabbitmq:5672")?;
    // Open a channel - None says let the library choose the channel ID.
    let rabbit_channel = rabbit_connection.open_channel(None)?;
    //
    // // // Declare the fanout exchange we will bind to.
    // // let exchange = rabbit_channel.exchange_declare(
    // //     ExchangeType::Direct,
    // //     "direct_logs",
    // //     ExchangeDeclareOptions::default(),
    // // )?;

    // Get a handle to the direct exchange on our channel.
    let rabbit_exchange = Exchange::direct(&rabbit_channel);

    // start loop for cron checks
    loop {
        for row_data in mk_lib_database_cron::mk_lib_database_cron_service_read(db_client).await.unwrap() {
            let mut time_delta: chrono::Duration;
            println!("row_data: {:?}", row_data);
            let cron_schedule: String = row_data.get("mm_cron_schedule");
            if cron_schedule == "Weekly" {
                time_delta = chrono::Duration::weeks(1);
            } else {
                let time_span_vector: Vec<&str> = cron_schedule.split(' ').collect();
                if time_span_vector[0] == "Days" {
                    time_delta = chrono::Duration::days(time_span_vector[1].parse().unwrap());
                } else if time_span_vector[0] == "Hours" {
                    time_delta = chrono::Duration::hours(time_span_vector[1].parse().unwrap());
                } else {
                    // time_span_vector[0] == "Minutes":
                    time_delta = chrono::Duration::minutes(time_span_vector[1].parse().unwrap());
                }
            }
            let date_check: DateTime<Utc> = Utc::now() - time_delta;
            let last_run: DateTime<Utc> = row_data.get("mm_cron_last_run");
            println!("date_check: {:?}, {:?}", date_check, last_run);
            if last_run < date_check {
                let cron_json = row_data.try_get::<&str, serde_json::Value>("mm_cron_json")?;
                rabbit_exchange.publish(Publish::with_properties("hello there".as_bytes(),
                                                                 cron_json["route_key"].to_string(),
                                                                 AmqpProperties::default().with_delivery_mode(2).with_content_type("text/plain".to_string())))?;

                // channel.basic_publish(exchange = row_data.get("mm_cron_json")("exchange_key"),
                //                       routing_key = row_data['mm_cron_json']['route_key'],
                //                       body = json.dumps(
                //                           {
                //                               'Type': row_data['mm_cron_json']['Type'],
                //                               'JSON': row_data['mm_cron_json']
                //                           }),
                //                       properties = pika.BasicProperties(
                //                           content_type ='text/plain',
                //                           delivery_mode = 2),
                //)
                mk_lib_database_cron::mk_lib_database_cron_time_update(db_client,
                                                                       row_data.get("mm_cron_guid")).await;
            }
            let uuid_cron: uuid::Uuid = row_data.get("mm_cron_guid");
            mk_lib_logging::mk_logging_post_elk("info",
                                                &uuid_cron.to_string(),
                                                "cron_checker").await;
        }
        sleep(Duration::from_secs(60)).await;
    }
    Ok(())
    // Code below can't be hit currently. So, drop the commands.
    // close the rabbit connection
    // rabbit_connection.close();
    // close the database
    // db_client.db_close();
}