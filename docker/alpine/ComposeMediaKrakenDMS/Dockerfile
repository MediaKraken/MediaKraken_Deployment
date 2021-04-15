# Download base image
FROM  th-registry-1.beaverbay.local:5000/mediakraken/mkbaseffmpeg:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This holds the dms app"

ARG ALPMIRROR
ARG PIPMIRROR

WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  go==1.15.10-r0 \
  go get https://github.com/anacrolix/dms \
  cifs-utils==6.12-r0 \
  curl==7.74.0-r1 \
  curl-dev==7.74.0-r1 \
  nfs-utils==2.5.2-r0 \
  postgresql-client \
  openssl==1.1.1k-r0 \
  alpine-sdk==1.0-r0 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  openldap==2.4.57-r1 \
  openldap-dev==2.4.57-r1 \
  jpeg==9d-r1 \
  jpeg-dev==9d-r1 \
  libxml2-dev==2.9.10-r6 \
  libxslt-dev==1.1.34-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r0 \
  net-snmp==5.9-r2 \
  net-snmp-dev==5.9-r2 \
  portaudio==190600.20161030-r1 \
  portaudio-dev==190600.20161030-r1 \
  postgresql-dev==13.2-r0 \
  python3-dev==3.8.8-r0 \
  openrc==0.42.1-r19 \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && apk del \
  alpine-sdk \
  curl-dev \
  jpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  openldap-dev \
  portaudio-dev \
  postgresql-dev \
  python3-dev \
  && apk add --no-cache \
  py3-setuptools==51.3.3-r0

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
