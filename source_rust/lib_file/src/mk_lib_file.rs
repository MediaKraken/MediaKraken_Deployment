use std::io;
use std::io::prelude::*;
use walkdir::{DirEntry, WalkDir};

pub fn mk_read_file_data(file_to_read: &str) -> io::Result<()> {
    let mut file_handle = std::fs::File::open(file_to_read)?;
    let mut buffer = String::new();
    file_handle.read_to_string(&mut buffer)?;
    Ok(())
}

fn is_hidden(entry: &DirEntry) -> bool {
    entry.file_name()
        .to_str()
        .map(|s| s.starts_with("."))
        .unwrap_or(false)
}

// "C:\\Users\\spoot\\Documents\\MediaKraken_Deployment\\source_rust\\bulk_themoviedb_netfetch"
pub fn mk_directory_walk(dir_path: &str) {
    let walker = WalkDir::new(dir_path).into_iter();
    for entry in walker.filter_entry(|e| !is_hidden(e)) {
        let entry = entry.unwrap();
        println!("{}", entry.path().display());
    }
}