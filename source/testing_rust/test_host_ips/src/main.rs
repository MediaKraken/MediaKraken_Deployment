use pnet::datalink;

// [V4(Ipv4Network { addr: 127.0.0.1, prefix: 8 }), V6(Ipv6Network { addr: ::1, prefix: 128 })]
// [V4(Ipv4Network { addr: 10.0.0.159, prefix: 24 }), V6(Ipv6Network { addr: fe80::a860:feff:fe84:2a0f, prefix: 64 })]
// [V4(Ipv4Network { addr: 172.22.97.113, prefix: 16 }), V6(Ipv6Network { addr: fe80::b4e4:f9ff:fedf:224e, prefix: 64 })]
// [V4(Ipv4Network { addr: 172.23.0.1, prefix: 16 }), V6(Ipv6Network { addr: fe80::42:7aff:fe44:352b, prefix: 64 })]
// [V4(Ipv4Network { addr: 172.17.0.1, prefix: 16 }), V6(Ipv6Network { addr: fe80::42:97ff:fe27:a92c, prefix: 64 })]
// [V6(Ipv6Network { addr: fe80::9c52:8ff:feff:3502, prefix: 64 })]

fn main() {
    for iface in datalink::interfaces() {
        println!("{:?} {:?}", iface.name, iface.ips);
    }
}