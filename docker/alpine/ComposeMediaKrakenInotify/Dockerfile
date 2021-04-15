# https://github.com/MediaKraken-Dependancies/docker-inotify
FROM alpine:3.13.5

LABEL maintainer="spootdev@gmail based on code by pstauffer@confirm.ch"

COPY init.sh /init.sh
RUN apk add --no-cache \
  busybox==1.32.1-r6 \
  curl==7.74.0-r1 \
  inotify-tools==3.20.11.0-r0 \
  && chmod 750 /init.sh

WORKDIR /tmp

CMD ["/init.sh"]
