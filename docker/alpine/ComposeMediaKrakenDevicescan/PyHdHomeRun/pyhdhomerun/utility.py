
from socket import inet_ntoa

def ip_int_to_ascii(ip_int):
    return inet_ntoa(hex(ip_int)[2:-1].zfill(8).decode('hex'))

def ip_ascii_to_int(ip):
    octets = [int(octet) for octet in ip.split('.')]

    if len(octets) != 4:
        raise Exception("IP [%s] does not have four octets." % (ip))

    encoded = ("%02x%02x%02x%02x" % (octets[0], octets[1], octets[2], octets[3]))
    return int(encoded, 16)

