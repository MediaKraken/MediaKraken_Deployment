FROM ubuntu:14.04

MAINTAINER Jason Rivers <docker@jasonrivers.co.uk>
ENV FACTORIO_SERVER_PORT=34197

WORKDIR /opt

COPY ./new_smart_launch.sh /opt/

VOLUME /opt/factorio/saves /opt/factorio/mods

EXPOSE 34197/udp
EXPOSE 27015/tcp

CMD ["./new_smart_launch.sh"]

ENV FACTORIO_BUILD \
    FACTORIO_AUTOSAVE_INTERVAL=2 \
    FACTORIO_AUTOSAVE_SLOTS=3 \
    FACTORIO_NO_AUTO_PAUSE=false \
    FACTORIO_WAITING=false \
    FACTORIO_MODE=normal \
    FACTORIO_SERVER_NAME="Factorio Server" \
    FACTORIO_SERVER_DESCRIPTION= \
    FACTORIO_SERVER_MAX_PLAYERS= \
    FACTORIO_SERVER_VISIBILITY_PUBLIC=true \
    FACTORIO_USER_USERNAME= \
    FACTORIO_USER_PASSWORD= \
    FACTORIO_SERVER_GAME_PASSWORD= \
    FACTORIO_SERVER_VERIFY_IDENTITY=false \
    FACTORIO_SERVER_VERSION=

RUN  apt-get update \
  && apt-get install -y wget xz-utils \
  && rm -rf /var/lib/apt/lists/*

## Pre-load the image with the stable version

RUN  wget -q -O - https://www.factorio.com/download-headless | grep -o -m1 "/get-download/.*/headless/linux64" | tee /tmp/factorioV | awk '{print "--no-check-certificate https://www.factorio.com"$1" -O /tmp/factorio.tar.xz"}' | xargs wget \
  && tar xf /tmp/factorio.tar.xz -C /opt \
  && rm -rf /tmp/factorio.tar.xz    \
  && cat /tmp/factorioV | sed 's/\/get-download\/\(.*\)\/headless\/linux64/\1/' >> /opt/factorio/currentVersion
