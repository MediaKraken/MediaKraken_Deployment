use shiplift::Docker;

fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

#[tokio::main]
async fn main() {
    let docker = Docker::new();
    println!("docker containers that are running");

    let result = docker.containers().list(&Default::default()).await;

    match result {
        Ok(images) => {
            for i in images {
                if i.names[0] == "/mkstack_reactor" {
                    print_type_of(&i.ports);
                    println!(
                        "{} {:?}",
                        i.id,
                        i.ports[0].private_port
                    );
                }
            }
        }
        Err(e) => eprintln!("Error: {}", e),
    }
}
