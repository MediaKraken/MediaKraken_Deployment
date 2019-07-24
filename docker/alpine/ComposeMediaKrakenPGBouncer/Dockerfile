# Download base image
FROM alpine:3.10

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This holds the image for pgbouncer"

ARG ALPMIRROR
ARG PIPMIRROR

# pip3 is installed with python3
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  c-ares \
  libevent \
  openssl \
  pgbouncer \
  && adduser -DHs /sbin/nologin metaman \
  && mkdir /run/postgresql

WORKDIR /
COPY wait-for-it-ash.sh ./
COPY entrypoint.sh ./
ENTRYPOINT ["./entrypoint.sh"]
