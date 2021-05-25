// attohttpc
use chrono::prelude::*;

pub fn mk_logging_post_elk(message_type:&str, message_text:&str,
                           index_name:&str) -> attohttpc::Result {
    let utc: DateTime<Utc> = Utc::now();
    let data = json!({"@timestamp": utc.format("%Y-%m-%dT%H:%M:%S.%f").to_string(),
        "message": message_text, "type": message_type, "user": {"id": "metaman"}});
    let resp = attohttpc::post(
        format!("http://th-elk-1.beaverbay.local:9200/%s/MediaKraken", index_name))
        .header("Content-Type", "application/json")
        .json(&data).send()?;
    println!("Status: {:?}", resp.status());
    println!("Headers:\n{:#?}", resp.headers());
    if resp.is_success() {
        println!("{}", resp.text()?);
    }
    Ok(())
}