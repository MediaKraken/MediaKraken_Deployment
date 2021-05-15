// launch the vs tools app otherwise can't compile (windows os only)
// cargo build --release

use postgres::{Client, NoTls, Error};

fn main() -> Result<(), Error> {
    let mut client = Client::connect("postgresql://postgres:metaman@localhost/postgres", NoTls)?;

    client.batch_execute("
        CREATE TABLE IF NOT EXISTS author (
            id              SERIAL PRIMARY KEY,
            name            VARCHAR NOT NULL,
            country         VARCHAR NOT NULL
            )
    ")?;

    client.batch_execute("
        CREATE TABLE IF NOT EXISTS book  (
            id              SERIAL PRIMARY KEY,
            title           VARCHAR NOT NULL,
            author_id       INTEGER NOT NULL REFERENCES author
            )
    ")?;

    Ok(())

}