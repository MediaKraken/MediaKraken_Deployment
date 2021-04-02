# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the pika app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  alpine-sdk \
  python3-dev==3.8.8-r0 \
  libressl==3.1.5-r0 \
  libressl-dev==3.1.5-r0 \
  cifs-utils==6.12-r0 \
  curl \
  curl-dev \
  nfs-utils==2.5.2-r0 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  openldap-dev \
  jpeg-dev \
  libxml2-dev==2.9.10-r6 \
  libxslt-dev==1.1.34-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  openldap-dev \
  portaudio-dev \
  krb5-dev \
  postgresql-client \
  py3-psycopg2 \
  py3-psutil \
  py3-babel \
  py3-requests \
  py3-uritemplate \
  py3-httplib2 \
  py3-setuptools \
  py3-curl \
  py3-natsort \
  openrc==0.42.1-r19 \
  rust \
  cargo \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  alpine-sdk \
  cargo \
  curl-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  libressl-dev \
  musl-dev \
  net-snmp-dev \
  python3-dev \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
