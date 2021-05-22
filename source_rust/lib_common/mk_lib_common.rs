fn print_type_of_variable<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}