use chrono::prelude::*;
use reqwest::StatusCode;

// attohttpc is not async
// pub fn mk_logging_post_elk(message_type:&str, message_text:&str,
//                            index_name:&str) -> attohttpc::Result {
//     let utc: DateTime<Utc> = Utc::now();
//     let data = serde_json::json!({"@timestamp": utc.format("%Y-%m-%dT%H:%M:%S.%f").to_string(),
//         "message": message_text, "type": message_type, "user": {"id": "metaman"}});
//     let resp = attohttpc::post(
//         format!("http://th-elk-1.beaverbay.local:9200/{}/MediaKraken", index_name))
//         .header("Content-Type", "application/json")
//         .json(&data).send()?;
//     println!("Status: {:?}", resp.status());
//     println!("Headers:\n{:#?}", resp.headers());
//     if resp.is_success() {
//         println!("{}", resp.text()?);
//     }
//     Ok(())
// }

pub async fn mk_logging_post_elk(message_type: &str, message_text: &str,
                                 index_name: &str) {
    let utc: DateTime<Utc> = Utc::now();
    let data = serde_json::json!({"@timestamp": utc.format("%Y-%m-%dT%H:%M:%S.%f").to_string(),
        "message": message_text, "type": message_type, "user": {"id": "metaman"}});
    // let resp = attohttpc::post(
    //     format!("http://th-elk-1.beaverbay.local:9200/{}/MediaKraken", index_name))
    //     .header("Content-Type", "application/json")
    //     .json(&data).send()?;
    // println!("Status: {:?}", resp.status());
    // println!("Headers:\n{:#?}", resp.headers());
    // if resp.is_success() {
    //     println!("{}", resp.text()?);
    // }
    let client = reqwest::Client::new();
    let resp = client.post(format!("http://th-elk-1.beaverbay.local:9200/{}/MediaKraken",
                                   index_name))
        .header("Content-Type", "application/json")
        .json(&data)
        .send()
        .await;
    println!("Status: {:?}", resp.status());
    // Ok(())
}