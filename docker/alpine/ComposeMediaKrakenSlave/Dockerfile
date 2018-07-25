# Download base image
FROM mediakraken/mkbasenodeffmpeg:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

ARG ALPMIRROR=dl-cdn.alpinelinux.org

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && echo '@edge http://nl.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories \
  && apk add --update \
  python \
  cifs-utils \
  nfs-utils \
  bash \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  libressl \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  nginx-mod-rtmp@edge \
  python3 \
  python3-dev \
  openrc \
  py3-service_identity \
  py3-setuptools \
  && pip3 install -r requirements.txt \
  && npm install -g castnow \
  && apk del \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  python3-dev \
  && apk add \
  py-setuptools \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/* \
  && rm -r /root/.npm \
  && rc-update add netmount \
  && rc-update add rpcbind

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
