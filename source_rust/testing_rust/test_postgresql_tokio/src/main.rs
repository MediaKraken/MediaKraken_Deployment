use tokio_postgres::{NoTls, Error};
// use serde::{Serialize, Deserialize};

fn print_type_of<T>(_: &T) {
    println!("Var Type: {}", std::any::type_name::<T>())
}

/*
{
    "Type": "Update Metadata",
    "program": "/mediakraken/async_metadata_themoviedb_updates.py",
    "route_key": "themoviedb",
    "exchange_key": "mkque_metadata_ex"
}
*/

// #[derive(Serialize, Deserialize, Debug)]
// struct CronJson {
//   cron_type: String,
//   program: String,
//   route_key: String,
//   ex_key: String
// }

#[tokio::main] // By default, tokio_postgres uses the tokio crate as its runtime.
async fn main() -> Result<(), Error> {
    // Connect to the database.
    let (client, connection) =
        tokio_postgres::connect("host=localhost user=postgres password=metaman", NoTls).await?;

    // The connection object performs the actual communication with the database,
    // so spawn it off to run on its own.
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    // Now we can execute a simple statement that just returns its parameter.
    let rows = client
        .query("SELECT $1::TEXT", &[&"hello world"])
        .await?;
    // And then check that we got back the same string we sent over.
    let value: &str = rows[0].get(0);
    assert_eq!(value, "hello world");

    for row in client.query("select mm_cron_guid, mm_cron_schedule, mm_cron_last_run,\
         mm_cron_json from mm_cron where mm_cron_enabled = False", &[]).await? {
        // let id: i32 = row.get(0);
        // let name: &str = row.get(1);
        // let data: Option<&[u8]> = row.get(2);
        //println!("found person: {} {} {:?}", id, name, data);
        println!("stuff: {:?}", row);

        let cron_json = row.try_get::<&str, serde_json::Value>("mm_cron_json")?;
        println!("ha: {:?}", cron_json["Type"]);
    }

    Ok(())
}