pub async fn mk_lib_database_cron_service_read() -> Result<(), Error> {
    let rows = client
        .query_one("select mm_cron_guid, mm_cron_schedule, mm_cron_last_run,\
         mm_cron_json from mm_cron where mm_cron_enabled = true")
        .await?;
    let mm_cron_json: &str = rows.try_get::<&str, serde_json::Value>("mm_cron_json");
}

// for row in client.query("SELECT id, name, data FROM person", &[])? {
//      let id: i32 = row.get(0);
//      let name: &str = row.get(1);
//      let data: Option<&[u8]> = row.get(2);
//      println!("found person: {} {} {:?}", id, name, data);
//  }

