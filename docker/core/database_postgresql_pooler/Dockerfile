# Download base image
FROM alpine:3.13.5

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This holds the image for pgbouncer"

ARG ALPMIRROR

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  busybox==1.32.1-r6 \
  c-ares==1.17.1-r1 \
  libevent==2.1.12-r1 \
  openssl==1.1.1k-r0 \
  pgbouncer==1.15.0-r0 \
  postgresql-client==13.2-r0 \
  && mkdir /run/postgresql \
  && chmod 777 /run/postgresql

#  && adduser -DHs /sbin/nologin metaman \

WORKDIR /
COPY wait-for-it-ash-busybox130.sh ./
COPY entrypoint.sh ./
EXPOSE 6432
ENTRYPOINT ["./entrypoint.sh"]
