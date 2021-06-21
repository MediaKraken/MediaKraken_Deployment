use pnet::datalink;
use shiplift::Docker;
use std::io;
use std::str;
use tokio::net::UdpSocket;

#[tokio::main]
async fn main() -> io::Result<()> {
    let mut mediakraken_ip: &str = "127.0.0.1";
    // loop through interfaces
    for iface in datalink::interfaces() {
        if iface.name == "ens18" {
            for source_ip in iface.ips.iter() {
                if source_ip.is_ipv4() {
                    println!("{:?}", source_ip);
                    let mediakraken_ip = iface.ips.iter().find(|ip| ip.is_ipv4())
                    .map(|ip| match ip.ip() {
                        IpAddr::V4(ip) => ip,
                        _ => unreachable!(),
                    }).unwrap();
                    println!("{:?}", mediakraken_ip);
                }
            }
        }
    let mut host_port: u64 = 8903;

    // Grab public port that the reactor is running on
    let docker = Docker::new();
    let result = docker.containers().list(&Default::default()).await;
    match result {
        Ok(images) => {
            for i in images {
                if i.names[0] == "/mkstack_reactor" {
                    host_port = i.ports[0].private_port;
                    break;
                }
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }
    // Begin the broadcast receive loop
    let sock = UdpSocket::bind("0.0.0.0:9101").await?;
    let mut buf= [0; 1024];
    loop {
        let (len, addr) = sock.recv_from(&mut buf).await?;
        if len == 25 {
            let net_string = match str::from_utf8(&buf[..25]) {
                Ok(v) => v,
                Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
            };
            if net_string == "who is MediaKrakenServer?"
            {
                println!("{:?} bytes received {:?} {:?}", len, addr, net_string);
                println!("{:?} mk port", host_port);

                let mk_address = format!("{}:{}", mediakraken_ip, host_port);
                println!("{:?} mk_address", mk_address);
                let len = sock.send_to(&mk_address.into_bytes(), addr).await?;
                println!("{:?} bytes sent", len);
            }
        }
    }
}
