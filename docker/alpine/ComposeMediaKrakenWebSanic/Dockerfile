# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This holds the image for the web server app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --no-cache \
  ack==3.4.0-r0 \
  curl==7.77.0-r1 \
  curl-dev==7.77.0-r1 \
  git==2.30.2-r0 \
  gcc==10.2.1_pre1-r3 \
  g++==10.2.1_pre1-r3 \
  krb5==1.18.3-r1 \
  krb5-dev==1.18.3-r1 \
  libstdc++==10.2.1_pre1-r3 \
  jpeg==9d-r1 \
  jpeg-dev==9d-r1 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  libxml2==2.9.10-r7 \
  libxml2-dev==2.9.10-r7 \
  libxslt==1.1.34-r0 \
  libxslt-dev==1.1.34-r0 \
  linux-headers==5.7.8-r0 \
  make==4.3-r0 \
  musl-dev==1.2.2-r1 \
  openrc==0.42.1-r20 \
  openssl==1.1.1k-r0 \
  openssl-dev==1.1.1k-r0 \
  py3-cffi==1.14.4-r0 \
  python3-dev==3.8.10-r0 \
  cifs-utils==6.13-r0 \
  nfs-utils==2.5.2-r0 \
  ca-certificates==20191127-r5 \
  py3-numpy==1.19.5-r0 \
  py3-psutil==5.8.0-r0 \
  rust==1.47.0-r2 \
  cargo==1.47.0-r2 \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install --no-cache-dir git+https://github.com/MediaKraken/sanic-auth \
  && apk del \
  cargo \
  curl-dev \
  gcc \
  g++ \
  git \
  jpeg-dev \
  krb5-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  make \
  musl-dev \
  linux-headers \
  python3-dev \
  openssl-dev \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

EXPOSE 8080
CMD ["/bin/ash"]
