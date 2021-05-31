// pub fn mk_download_file_from_url(url_to_download: &str, file_save_path: &str) -> attohttpc::Result {
//     let resp = attohttpc::get(url_to_download).send()?;
//     println!("Status: {:?}", resp.status());
//     println!("Headers:\n{:#?}", resp.headers());
//     if resp.is_success() {
//         let file = std::fs::File::create(file_save_path)?;
//         let n = resp.write_to(file)?;
//         println!("Wrote {} bytes to the file.", n);
//     }
//     Ok(())
// }

pub async fn mk_download_file_from_url(url_to_download: &str, file_save_path: &str) {
    let response = reqwest::get(url_to_download).await;
    let path = std::path::Path::new(file_save_path);
    let mut file_handle = match std::fs::File::create(&path) {
        Err(why) => panic!("couldn't create {}", why),
        Ok(file) => {
            let content = response.bytes().await;
            file_handle.write_all(content);
        }
    };
}

// wait_seconds - 120 typically
pub async fn mk_network_service_available(host_dns: &str, host_port: &str,
                                          wait_seconds: &str) {
    if std::path::Path::new("/mediakraken/wait-for-it-ash-busybox130.sh").exists() {
        std::process::Command::new("/mediakraken/wait-for-it-ash-busybox130.sh")
            .arg("-h")
            .arg(host_dns)
            .arg("-p")
            .arg(host_port)
            .arg("-t")
            .arg(wait_seconds)
            .spawn();
    } else if std::path::Path::new("/mediakraken/wait-for-it-ash.sh").exists() {
        std::process::Command::new("/mediakraken/wait-for-it-ash.sh")
            .arg("-h")
            .arg(host_dns)
            .arg("-p")
            .arg(host_port)
            .arg("-t")
            .arg(wait_seconds)
            .spawn();
    } else {
        std::process::Command::new("/mediakraken/wait-for-it-bash.sh")
            .arg("-h")
            .arg(host_dns)
            .arg("-p")
            .arg(host_port)
            .arg("-t")
            .arg(wait_seconds)
            .spawn();
    }
}