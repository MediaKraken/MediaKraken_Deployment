FROM gliderlabs/alpine:3.3

MAINTAINER packeteer <packeteer@gmail.com>

RUN apk-install openldap openldap-clients openldap-back-hdb openldap-back-bdb ldapvi

EXPOSE 389 636

CMD ulimit -n 8192 && /usr/sbin/slapd -d 256 -u ldap -g ldap -F /etc/openldap/slapd.d
