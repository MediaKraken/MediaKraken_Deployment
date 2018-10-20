FROM gliderlabs/alpine:3.8

MAINTAINER packeteer <packeteer@gmail.com>

ARG ALPMIRROR
ARG PIPMIRROR

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update openldap openldap-clients openldap-back-hdb openldap-back-bdb ldapvi

EXPOSE 389 636

CMD ulimit -n 8192 && /usr/sbin/slapd -d 256 -u ldap -g ldap -F /etc/openldap/slapd.d
