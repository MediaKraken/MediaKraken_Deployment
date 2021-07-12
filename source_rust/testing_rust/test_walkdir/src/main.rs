use walkdir::{DirEntry, WalkDir};

fn is_hidden(entry: &DirEntry) -> bool {
    entry.file_name()
         .to_str()
         .map(|s| s.starts_with("."))
         .unwrap_or(false)
}

fn main() {
    let walker = WalkDir::new("C:\\Users\\spoot\\Documents\\MediaKraken_Deployment\\docker\\core\\tmdb_netfetch_bulk").into_iter();
    for entry in walker.filter_entry(|e| !is_hidden(e)) {
        let entry = entry.unwrap();
        println!("{}", entry.path().display());
    }
}