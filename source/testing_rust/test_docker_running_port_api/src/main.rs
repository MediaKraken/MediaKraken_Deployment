use shiplift::Docker;

#[tokio::main]
async fn main() {
    let docker = Docker::new();
    println!("docker containers that are running");

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
}
