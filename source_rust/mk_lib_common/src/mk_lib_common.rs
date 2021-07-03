pub fn print_type_of_variable<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}

// // cargo test -- --show-output
// #[cfg(test)]
// mod test_mk_lib_common {
//     use super::*;
//
//     macro_rules! aw {
//     ($e:expr) => {
//         tokio_test::block_on($e)
//     };
//   }
//
//     // doesn't return anything, so, can't really test it
//     // #[test]
//     // fn test_print_type_of_variable() {
//     //     let res = 32;
//     //     let result = print_type_of_variable(&res).unwrap();
//     // }
//
// }
