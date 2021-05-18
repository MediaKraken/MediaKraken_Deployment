use pnet::datalink;

fn main() {
    for iface in datalink::interfaces() {
        println!("{:?}", iface.ips);
    }
}