# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_ffmpeg:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the transcoding app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

# don't remove py3-pip as it breaks package lookup
RUN apk add --no-cache \
  cifs-utils==6.13-r0 \
  nfs-utils==2.5.2-r0 \
  libressl==3.1.5-r0 \
  libressl-dev==3.1.5-r0 \
  net-snmp==5.9-r3 \
  python3==3.8.10-r0 \
  py3-pip==20.3.4-r0 \
  openrc==0.42.1-r20 \
  gcc==10.2.1_pre1-r3 \
  python3-dev==3.8.10-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r1 \
  krb5==1.18.3-r1 \
  krb5-dev==1.18.3-r1 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  rust==1.47.0-r2 \
  cargo==1.47.0-r2 \
  && pip3 install --no-cache-dir --upgrade pip==21.0.1 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
    cargo \
    gcc \
    krb5-dev \
    python3-dev \
    libffi-dev \
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
