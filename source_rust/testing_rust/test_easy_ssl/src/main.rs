use easy_ssl::{builder,common,generate_as_files};

// tries to install openssl and compile with it

fn main(){

    let mut build = builder::Builder::new();

    build.set_key_path("D://workstation/expo/rust/fdb/cert/keys/key.pem".to_string());
    build.set_certificate_path("D://workstation/expo/rust/fdb/cert/keys/cert.pem".to_string());
    build.set_key_size(4048);

    build.issuer.set_country("IN".to_string());
    build.issuer.set_state("UP".to_string());
    build.issuer.set_location("GZB".to_string());
    build.issuer.set_org("DAACHI".to_string());
    build.issuer.set_common_name("https://daachi.in".to_string());

    build.subject.set_country("IN".to_string());
    build.subject.set_state("UP".to_string());
    build.subject.set_location("GZB".to_string());
    build.subject.set_org("DAACHI".to_string());
    build.subject.set_common_name("127.0.0.1".to_string());

    match generate_as_files(&mut build) {
        Ok(r)=>{
            println!("{:?}",r);
        },
        Err(e)=>{
            println!("erro : {:?}",e);
            common::error("failed-generate_as_vec");
        }
    }

}