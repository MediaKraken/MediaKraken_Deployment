# https://github.com/rlesouef/alpine-transmission

FROM alpine:3.13.5

LABEL maintainer="Open Source Services [opensourceservices.fr]"

ARG ALPMIRROR
ARG PIPMIRROR

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
    && apk add --no-cache \
    busybox==1.32.1-r6 \
    transmission-daemon==3.00-r2

RUN mkdir -p /transmission/downloads \
  && mkdir -p /transmission/incomplete \
  && mkdir -p /etc/transmission-daemon

COPY src/ .

VOLUME ["/etc/transmission-daemon"]
VOLUME ["/transmission/downloads"]
VOLUME ["/transmission/incomplete"]

EXPOSE 9091 51413/tcp 51413/udp

ENV USERNAME admin
ENV PASSWORD password

RUN chmod +x /start-transmission.sh
CMD ["/start-transmission.sh"]
