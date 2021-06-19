use shiplift::Docker;
use std::io;
use std::str;
use tokio::net::UdpSocket;
use std::env;

#[tokio::main]
async fn main() -> io::Result<()> {
    // grab swarm or host port
    let mut mediakraken_ip: &str = "127.0.0.1";
    let mut host_port: u64 = 8903;
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
