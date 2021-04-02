# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the hardware app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  eudev-dev \
  gcc \
  git \
  linux-headers==5.7.8-r0 \
  libffi-dev==3.3-r2 \
  libusb-dev \
  libxml2-dev==2.9.10-r6 \
  libxslt-dev==1.1.34-r0 \
  musl-dev \
  openssl-dev \
  python3-dev==3.8.8-r0 \
  rust \
  cargo \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install --no-cache-dir git+https://github.com/MediaKraken/phue \
  && rm requirements.txt \
  && apk del \
  cargo \
  gcc \
  git \
  linux-headers \
  musl-dev \
  python3-dev==3.8.8-r0

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
