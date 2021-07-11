pub async fn mk_lib_database_notification_insert(client: &tokio_postgres::Client,
                                                 mm_notification_text: String,
                                                 mm_notification_dismissable: bool)
                                                 -> Result<bool, Error> {
    let row = client
        .query_one("insert into mm_notification (mm_notification_guid, \
        mm_notification_text, \
        mm_notification_time = NOW(), \
        mm_notification_dismissable) \
        values ($1, $2, $3)",
                   &[&Uuid::new_v4(), &mm_notification_text,
                       &mm_notification_dismissable]).await?;
    Ok()
}