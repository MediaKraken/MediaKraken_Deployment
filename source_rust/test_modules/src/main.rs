extern crate lib_logging;

fn main() {
   println!("inside main of test ");
   lib_logging::mk_lib_logging::mk_logging_post_elk("info", "test message", "mk_test");
}