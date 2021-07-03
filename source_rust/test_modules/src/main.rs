extern crate mk_lib_logging;

fn main() {
   println!("inside main of test ");
   mk_lib_logging::mk_lib_logging::mk_logging_post_elk("info", "test message", "mk_test");
}