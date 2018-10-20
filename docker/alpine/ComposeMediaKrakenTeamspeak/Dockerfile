### Alpine requires glibc to be present in the system below link to fficial repository
### https://github.com/sgerrand/alpine-pkg-glibc
### Based on https://github.com/pozgo/docker-teamspeak
FROM alpine:3.8

ARG ALPMIRROR
ARG PIPMIRROR

ENV     TS3_VERSION=3.0.13.8 \
        GLIBC_VERSION='2.26-r0'

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
    && apk --no-cache add ca-certificates wget; \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://raw.githubusercontent.com/sgerrand/alpine-pkg-glibc/master/sgerrand.rsa.pub; \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk; \
    apk add glibc-${GLIBC_VERSION}.apk; \
    apk add --update bzip2; \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/* /glibc-${GLIBC_VERSION}.apk; \
    wget http://dl.4players.de/ts/releases/${TS3_VERSION}/teamspeak3-server_linux_amd64-${TS3_VERSION}.tar.bz2 -O /tmp/teamspeak.tar.bz2

COPY container-files /

ENTRYPOINT ["/bootstrap.sh"]

EXPOSE 9987/udp 10011 30033
