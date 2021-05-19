use std::fs::File;

pub fn mk_download_file_from_url(url_to_download:&str, file_save_path:&str) -> attohttpc::Result {
    let resp = attohttpc::get(url_to_download).send()?;
    println!("Status: {:?}", resp.status());
    println!("Headers:\n{:#?}", resp.headers());
    if resp.is_success() {
        let file = File::create(file_save_path)?;
        let n = resp.write_to(file)?;
        println!("Wrote {} bytes to the file.", n);
    }
    Ok(())
}
