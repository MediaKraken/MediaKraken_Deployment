use std::io::Read;

pub fn mk_decompress_gzip(archive_file: &str) -> Result<String, std::io::Error> {
    let file_handle = std::fs::File::open(archive_file)?;
    let mut gz = flate2::read::GzDecoder::new(file_handle);
    let mut gz_data = String::new();
    gz.read_to_string(&mut gz_data)?;
    Ok(gz_data)
}

pub fn mk_decompress_zip(archive_file: &str, write_to_file: bool,
                         remove_zip: bool) -> Result<String, std::io::Error> {
    let file_handle = std::fs::File::open(archive_file)?;
    let mut gz = flate2::read::ZlibDecoder::new(file_handle);
    let mut gz_data = String::new();
    gz.read_to_string(&mut gz_data)?;
    if write_to_file {
        std::fs::write("/tmp/foo", gz_data).expect("Unable to write file");
    }
    if remove_zip {
        std::fs::remove_file(archive_file)?;
    }
    Ok(gz_data)
}

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