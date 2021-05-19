use std::fs::File;
use flate2::read::GzDecoder;
use std::io::prelude::*;

pub fn mk_decompress_gzip(archive_file:&str) -> Result<String, std::io::Error> {
    let file_handle = File::open(archive_file)?;
    let mut gz = GzDecoder::new(file_handle);
    let mut gz_data = String::new();
    gz.read_to_string(&mut gz_data)?;
    Ok(gz_data)
}
