# Download base image
FROM alpine:3.8

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This holds the image for pgbouncer"

ARG ALPMIRROR

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  c-ares \
  libevent \
  openssl \
  pgbouncer=1.7.2-r4 \
  postgresql-client \
  && mkdir /run/postgresql \
  && chmod 777 /run/postgresql

#  && adduser -DHs /sbin/nologin metaman \

WORKDIR /
COPY wait-for-it-ash.sh ./
COPY entrypoint.sh ./
ENTRYPOINT ["./entrypoint.sh"]
