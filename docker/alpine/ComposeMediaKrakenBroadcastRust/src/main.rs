use shiplift::Docker;
use std::io;
use std::str;
use tokio::net::UdpSocket;
use std::env;

#[tokio::main]
async fn main() -> io::Result<()> {
    // grab swarm or host port
    if env::var("SWARMIP") != "None" {
        let mediakraken_ip = env::var("SWARMIP");
    }
    else {
        let mediakraken_ip = env::var("HOST_IP");
    }
    // Grab public port that the reactor is running on
    let docker = Docker::new();
    let result = docker.containers().list(&Default::default()).await;
    match result {
        Ok(images) => {
            for i in images {
                if i.names[0] == "/mkstack_reactor" {
                    let host_port = i.ports[0].private_port;
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
                                let mk_address = b"10.0.0.141:{}" % host_port;
                                println!("{:?} mk_address", mk_address);
                                let len = sock.send_to(mk_address, addr).await?;
                                println!("{:?} bytes sent", len);
                            }
                        }
                    }
                }
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }
}
