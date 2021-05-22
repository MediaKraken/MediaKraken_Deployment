use postgres::{Client, Error, NoTls};


pub fn mk_lib_database_open(database_password: &str) -> Result<(), Error> {
    let mut client = Client::connect("postgresql://postgres:metaman@mkstack_database/postgres", NoTls)?;
}