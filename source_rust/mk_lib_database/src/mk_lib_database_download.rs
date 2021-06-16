use tokio_postgres::Error;
use uuid::Uuid;

pub async fn mk_lib_database_download_exists(client: &tokio_postgres::Client,
                                             metadata_provider: String,
                                             metadata_que_type: i16,
                                             metadata_provider_id: i32)
                                             -> Result<bool, Error> {
    let row = client
        .query_one("select exists(select 1 from mm_download_que \
        where mdq_provider_id = $1 and mdq_provider = $2 \
        and mdq_que_type = $3 and mdq_status != 'Search' limit 1) \
        as found_record limit 1",
                   &[&metadata_provider_id, &metadata_provider, &metadata_que_type]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}

pub async fn mk_lib_database_download_insert(client: &tokio_postgres::Client,
                                             metadata_provider: String,
                                             metadata_que_type: i16,
                                             metadata_new_uuid: Uuid,
                                             metadata_provider_id: i32,
                                             metadata_status: String)
                                             -> Result<bool, Error> {
    let row = client
        .query_one("insert into mm_download_que (mdq_id, \
        mdq_provider, \
        mdq_que_type, \
        mdq_new_uuid, \
        mdq_provider_id, \
        mdq_status) \
        values ($1, $2, $3, $4, $5, $6)",
                   &[&Uuid::new_v4(), &metadata_provider, &metadata_que_type,
                       &metadata_new_uuid, &metadata_provider_id, &metadata_status]).await?;
    let id: bool = row.get("found_record");
    Ok(id)
}

// Uuid::new_v4();
// new_guid = uuid.uuid4()
// await db_conn.execute('insert into mm_download_que (mdq_id,'
//                       ' mdq_provider,'
//                       ' mdq_que_type,'
//                       ' mdq_new_uuid,'
//                       ' mdq_provider_id,'
//                       ' mdq_status)'
//                       ' values ($1, $2, $3, $4, $5, $6)',
//                       new_guid, provider, que_type, down_new_uuid,
//                       down_json['ProviderMetaID'], down_json['Status'])

// // cargo test -- --show-output
// #[cfg(test)]
// mod test_mk_lib_common {
//     use super::*;
//
//     macro_rules! aw {
//     ($e:expr) => {
//         tokio_test::block_on($e)
//     };
//   }
// }