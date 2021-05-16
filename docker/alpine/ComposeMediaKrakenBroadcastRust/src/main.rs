use shiplift::Docker;
use std::io;
use std::str;
use tokio::net::UdpSocket;

#[tokio::main]
async fn main() -> io::Result<()> {
    let docker = Docker::new();
    let result = docker.containers().list(&Default::default()).await;
    match result {
        Ok(images) => {
            for i in images {
                if i.names[0] == "/mkstack_reactor" {
                    println!(
                        "{} {:?}",
                        i.id,
                        i.ports
                    );
                }
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }

    let sock = UdpSocket::bind("0.0.0.0:9101").await?;
    let mut buf = [0; 1024];
    loop {
        let (len, addr) = sock.recv_from(&mut buf).await?;
        if len == 25 {
            let net_string = match str::from_utf8(&buf[..25]) {
                Ok(v) => v,
                Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
            };
            if net_string == "who is MediaKrakenServer?"
            {
                println!("{:?} bytes received from {:?} {:?}", len, addr, net_string);
                let len = sock.send_to(b"10.0.0.141:8903", addr).await?;
                println!("{:?} bytes sent", len);
            }
        }
    }
}
