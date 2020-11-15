# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase3121py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main server app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  alpine-sdk \
  libffi-dev \
  openssl \
  openssl-dev \
  cifs-utils \
  curl-dev \
  nfs-utils \
  openldap-dev \
  jpeg-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  openldap-dev \
  openrc \
  portaudio-dev \
  py3-psycopg2 \
  py3-psutil \
  py3-babel \
  py3-service_identity \
  py3-requests \
  py3-uritemplate \
  py3-httplib2 \
  py3-setuptools \
  py3-curl \
  py3-natsort \
  python3-dev \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  alpine-sdk \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  openssl-dev \
  musl-dev \
  net-snmp-dev \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
