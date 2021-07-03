// error[E0554]: `#![feature]` may not be used on the stable release channel

#![feature(proc_macro_span)]
use inline_python::python;

fn main() {
    let who = "world";
    let n = 5;
    python! {
        for i in range('n):
            print(i, "Hello", 'who)
        print("Goodbye")
    }
}