use tokio::net::UdpSocket;
use std::io;
use std::str;

#[tokio::main]
async fn main() -> io::Result<()> {
    let sock = UdpSocket::bind("0.0.0.0:9101").await?;
    let mut buf = [0; 1024];
    loop {
        let (len, addr) = sock.recv_from(&mut buf).await?;
        if len == 25 {
            let s = match str::from_utf8(&buf[..25]) {
                Ok(v) => v,
                Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
            };
            if s == "who is MediaKrakenServer?"
            {
                println!("{:?} bytes received from {:?} {:?}", len, addr, s);

                let len = sock.send_to(b"10.0.0.141:8903", addr).await?;
                println!("{:?} bytes sent", len);
            }
        }
    }
}
