# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbaseffmpeg:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the transcoding app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

RUN apk add --no-cache \
  cifs-utils \
  nfs-utils \
  libressl \
  libressl-dev \
  net-snmp \
  python3 \
  py3-pip \
  openrc \
  gcc \
  python3-dev \
  linux-headers \
  musl-dev \
  krb5-dev \
  libffi-dev \
  rust \
  cargo \
  && pip3 install --upgrade pip \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
    gcc \
    python3-dev \
    linux-headers \
    musl-dev \
    libressl-dev \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
