// launch the vs tools app otherwise can't compile (windows os only)
// cargo build --release

fn main() {
    let a: u64 = 9000;
    let host_host = "10.0.0.141:";

    //let data = concat!(host_host, a.to_string());
    let data2 = format!("{}{}", host_host, a.to_string());
    println!("{}", data2)
}