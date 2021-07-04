use amiquip::{Connection, ConsumerMessage, ConsumerOptions, QueueDeclareOptions, Result};

fn main() -> Result<()> {
    // Open connection.
    let mut connection = Connection::insecure_open("amqp://guest:guest@mkstack_rabbitmq:5672")?;

    // Open a channel - None says let the library choose the channel ID.
    let channel = connection.open_channel(None)?;

    // Declare the "hello" queue.
    let queue = channel.queue_declare("hello", QueueDeclareOptions::default())?;

    // Start a consumer.
    let consumer = queue.consume(ConsumerOptions::default())?;

    for (i, message) in consumer.receiver().iter().enumerate() {
        match message {
            ConsumerMessage::Delivery(delivery) => {
                let body = String::from_utf8_lossy(&delivery.body);
                println!("({:>3}) Received [{}]", i, body);
                consumer.ack(delivery)?;
            }
            other => {
                println!("Consumer ended: {:?}", other);
                break;
            }
        }
    }
    connection.close()
}