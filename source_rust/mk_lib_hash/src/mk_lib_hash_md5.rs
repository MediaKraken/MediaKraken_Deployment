use md5::{Md5, Digest};
use std::fs;

pub fn mk_file_hash_md5(file_to_read: &str) -> io::Result<()> {
    let mut file = fs::File::open(&file_to_read)?;
    let hash = md5::digest_reader(&mut file)?;
    Ok(hash)
}