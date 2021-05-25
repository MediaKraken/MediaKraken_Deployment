use chrono::prelude::*;
use tokio::time::{Duration, sleep};
use tokio_postgres::{Error, NoTls};

#[path = "../../../../source_rust/lib_logging/mk_lib_logging.rs"]
mod mk_lib_logging;
#[path = "../../../../source_rust/lib_database/mk_lib_database.rs"]
mod mk_lib_database;
#[path = "../../../../source_rust/lib_database/mk_lib_database_cron.rs"]
mod mk_lib_database_cron;
#[path = "../../../../source_rust/lib_network/mk_lib_network.rs"]
mod mk_lib_network;

#[tokio::main]
fn main() -> Result<(), Box<dyn Error>> {
    // start logging
    mk_lib_logging::mk_logging_post_elk("info",
                                        "START",
                                        "cron_checker");
    // grab db password
    match env::var("POSTGRES_PASSWORD") {
        Ok(db_pass) => println!("{:?}", db_pass),
        Err(e) => println!("couldn't interpret {}", e),
    }
    // open the database
    let db_client = mk_lib_database::mk_lib_database_open(db_pass);

    // fire off wait for it script to verify rabbitmq is available
    mk_lib_network::mk_network_service_available("mkstack_rabbitmq",
                                                 "5672", "120");

//     credentials = pika.PlainCredentials('guest', 'guest')
//     parameters = pika.ConnectionParameters('mkstack_rabbitmq',
//                                            socket_timeout = 30, credentials = credentials)
//     connection = pika.BlockingConnection(parameters)
//     channel = connection.channel()

    // start loop for cron checks
    loop {
        for row_data in mk_lib_database_cron::mk_lib_database_cron_service_read(db_client) {
            let mut time_delta;
            if row_data.get("mm_cron_schedule") == "Weekly" {
                time_delta = Duration::weeks(1);
            } else {
                let time_span_vector: Vec<&str>
                    = row_data.get("mm_cron_schedule").split(' ').collect();
                if time_span_vector[0] == "Days" {
                    time_delta = Duration::days(time_span_vector[1]);
                } else if time_span_vector[0] == "Hours" {
                    time_delta = Duration::hours(time_span_vector[1]);
                } else {
                    // time_span_vector[0] == "Minutes":
                    time_delta = Duration::minutes(time_span_vector[1]);
                }
            }
            let utc: DateTime<Utc> = Utc::now();
            let date_check = utc - time_delta;
            if row_data.get("mm_cron_last_run") < date_check {
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
            }
            db_connection.db_cron_time_update(row_data.get("mm_cron_name"));
            db_connection.db_commit();
        }
        mk_lib_logging::mk_logging_post_elk("info",
                                            row_data,
                                            "cron_checker");
        sleep(Duration::from_secs(60)).await;
    }
    // close the pika connection
    //     connection.close()
    // close the database
    //     db_connection.db_close()
}