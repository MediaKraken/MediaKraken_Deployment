use shiplift::Docker;

#[tokio::main]
async fn main() {
    let docker = Docker::new();
    println!("docker images in stock");

    let result = docker.containers().list(&Default::default()).await;

    match result {
        Ok(images) => {
            for i in images {
                println!(
                    "{} {} {:?} {}",
                    i.id,
                    i.created,
                    i.labels.unwrap_or_else(|| vec!["none".into()]),
                    i.ports
                );
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }
}
