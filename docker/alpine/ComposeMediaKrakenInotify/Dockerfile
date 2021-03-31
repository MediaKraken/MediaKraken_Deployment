# https://github.com/MediaKraken-Dependancies/docker-inotify
FROM alpine:3.13.3

LABEL maintainer="spootdev@gmail based on code by pstauffer@confirm.ch"

COPY init.sh /init.sh
RUN apk add --no-cache curl inotify-tools && \
    chmod 750 /init.sh

WORKDIR /tmp

CMD ["/init.sh"]
