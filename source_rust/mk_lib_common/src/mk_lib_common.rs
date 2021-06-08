pub fn print_type_of_variable<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

// cargo test -- --show-output
#[cfg(test)]
mod test_mk_lib_common {
    use super::*;

    macro_rules! aw {
    ($e:expr) => {
        tokio_test::block_on($e)
    };
  }
}
