# Download base image
FROM mediakraken/mkbasenode:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the GrapeJS app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  python \
  bash \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  libressl \
  musl-dev \
  python3 \
  python3-dev \
  openrc \
  py3-service_identity \
  py3-setuptools \
  && npm install -g grapesjs \
  && apk del \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  python3-dev \
  && apk add \
  py-setuptools \
  && rm -rf /var/cache/apk/* \
  && rm -r /root/.npm

CMD ["/bin/ash"]
