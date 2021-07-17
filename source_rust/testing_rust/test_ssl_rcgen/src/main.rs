use rcgen::generate_simple_self_signed;

fn main() {
    let subject_alt_names = vec!["www.mediakraken.org".to_string(),
                                 "localhost".to_string()];

    let cert = generate_simple_self_signed(subject_alt_names).unwrap();
    println!("{}", cert.serialize_pem().unwrap());
    println!("{}", cert.serialize_private_key_pem());
}