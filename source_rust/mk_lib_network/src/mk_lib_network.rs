use std::io::Cursor;
use std::str;
type Result<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;

pub async fn mk_data_from_url(url: String) -> Result<String> {
    let response = reqwest::get(url).await?;
    let content = response.bytes().await?;
    Ok(str::from_utf8(&content).unwrap().to_string())
}

pub async fn mk_download_file_from_url(url: String, file_name: String) -> Result<()> {
    let response = reqwest::get(url).await?;
    let mut file = std::fs::File::create(file_name)?;
    let mut content =  Cursor::new(response.bytes().await?);
    std::io::copy(&mut content, &mut file)?;
    Ok(())
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
            .spawn().unwrap();
    } else if std::path::Path::new("/mediakraken/wait-for-it-ash.sh").exists() {
        std::process::Command::new("/mediakraken/wait-for-it-ash.sh")
            .arg("-h")
            .arg(host_dns)
            .arg("-p")
            .arg(host_port)
            .arg("-t")
            .arg(wait_seconds)
            .spawn().unwrap();
    } else {
        std::process::Command::new("/mediakraken/wait-for-it-bash.sh")
            .arg("-h")
            .arg(host_dns)
            .arg("-p")
            .arg(host_port)
            .arg("-t")
            .arg(wait_seconds)
            .spawn().unwrap();
    }
}

// cargo test -- --show-output
#[cfg(test)]
mod test_mk_lib_network {
    use super::*;

    macro_rules! aw {
    ($e:expr) => {
        tokio_test::block_on($e)
    };
  }

    #[test]
    fn test_mk_download_file_from_url() {
        let res = aw!(mk_download_file_from_url(
            "https://github.com/MediaKraken/MediaKraken_Deployment/raw/master/LICENSE".to_string(),
            "license.md".to_string()));
        assert!(res.is_ok());
    }
}
