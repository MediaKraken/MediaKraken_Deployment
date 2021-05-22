use std::io;
use std::io::prelude::*;
use std::fs::File;

pub fn mk_read_file_data(file_to_read:&str) -> io::Result<()> {
    let mut file_handle = File::open(file_to_read)?;
    let mut buffer = String::new();
    file_handle.read_to_string(&mut buffer)?;
    Ok(())
}