# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the image for the web server app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  ack \
  curl-dev \
  git \
  gcc \
  g++ \
  krb5-dev \
  libstdc++ \
  jpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  make \
  musl-dev \
  openrc \
  openssl-dev \
  py3-cffi \
  python3-dev \
  cifs-utils \
  nfs-utils \
  ca-certificates \
  openssl \
  py3-numpy \
  py3-psutil \
  rust \
  cargo \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install --no-cache-dir git+https://github.com/MediaKraken/sanic-auth \
  && apk del \
  gcc \
  g++ \
  git \
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
