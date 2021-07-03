# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the pika app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apk add --no-cache \
  alpine-sdk==1.0-r0 \
  python3-dev==3.8.10-r0 \
  libressl==3.1.5-r0 \
  libressl-dev==3.1.5-r0 \
  cifs-utils==6.13-r0 \
  curl==7.77.0-r1 \
  curl-dev==7.77.0-r1 \
  nfs-utils==2.5.2-r0 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  openldap==2.4.57-r1 \
  openldap-dev==2.4.57-r1 \
  jpeg==9d-r1 \
  jpeg-dev==9d-r1 \
  libxml2-dev==2.9.10-r7 \
  libxslt-dev==1.1.34-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r1 \
  net-snmp==5.9-r3 \
  net-snmp-dev==5.9-r3 \
  portaudio-dev==190600.20161030-r1 \
  krb5==1.18.3-r1 \
  krb5-dev==1.18.3-r1 \
  postgresql-client==13.3-r0 \
  py3-psycopg2==2.8.6-r0 \
  py3-psutil==5.8.0-r0 \
  py3-babel==2.8.0-r1 \
  py3-requests==2.25.1-r1 \
  py3-uritemplate==3.0.1-r0 \
  py3-httplib2==0.18.1-r0 \
  py3-setuptools==51.3.3-r0 \
  py3-curl==7.43.0.6-r0 \
  py3-natsort==7.1.1-r0 \
  openrc==0.42.1-r20 \
  rust==1.47.0-r2 \
  cargo==1.47.0-r2 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  alpine-sdk \
  cargo \
  curl-dev \
  krb5-dev \
  jpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  libressl-dev \
  musl-dev \
  net-snmp-dev \
  python3-dev \
  openldap-dev \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
