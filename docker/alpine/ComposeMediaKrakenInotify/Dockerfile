# https://github.com/MediaKraken-Dependancies/docker-inotify
FROM alpine:3.8

MAINTAINER spootdev@gmail based on code by pstauffer@confirm.ch

ADD init.sh /init.sh
RUN apk --update upgrade && \
    apk add --update curl inotify-tools && \
    rm -rf /var/cache/apk/* && \
    chmod 750 /init.sh

WORKDIR /tmp

CMD ["/init.sh"]
