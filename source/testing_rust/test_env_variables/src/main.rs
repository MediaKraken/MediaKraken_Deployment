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

    match env::var("PATH") {
        Ok(val) => println!("{:?}", val),
        Err(e) => println!("couldn't interpret {}", e),
    }

    match env::var("SWARMIP") {
        Ok(val) => println!("{:?}", val),
        Err(e) => println!("couldn't interpret {}", e),
    }

    let data = env::var_os("OS");
    println!("{:?}", data);

    match env::var("SWARMIP") {
    Ok(mediakraken_ip) => {
        println!("{:?}", mediakraken_ip);
        },
    Err(e) => {
        println!("couldn't interpret swarm {}", e);
        match env::var("HOST_IP") {
            Ok(mediakraken_ip) => {
                println!("{:?}", mediakraken_ip);
                },
            Err(e) => {
                println!("couldn't interpret host {}", e);
                }
            }
        }
    }

}
