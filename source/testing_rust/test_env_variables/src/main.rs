fn main() {
use std::env;

// these seem to return the same things
for (key, value) in env::vars_os() {
    println!("{:?}: {:?}", key, value);
}

for (key, value) in env::vars() {
    println!("{:?}: {:?}", key, value);
}

let key = "OS";
match env::var_os(key) {
    Some(val) => println!("{}: {:?}", key, val),
    None => println!("{} is not defined in the environment.", key)
}

let key = "PATH";
match env::var(key) {
    Ok(val) => println!("{}: {:?}", key, val),
    Err(e) => println!("couldn't interpret {}: {}", key, e),
}
}