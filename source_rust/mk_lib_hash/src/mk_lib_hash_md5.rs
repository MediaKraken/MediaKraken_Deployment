use sha1::{Sha1, Digest};
use std::fs;

let mut file = fs::File::open(&path)?;
let hash = Sha1::digest_reader(&mut file)?;