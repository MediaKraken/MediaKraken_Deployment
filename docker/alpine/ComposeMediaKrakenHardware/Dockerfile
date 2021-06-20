# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the hardware app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apk add --no-cache \
  eudev==3.2.9-r3 \
  eudev-dev==3.2.9-r3 \
  gcc==10.2.1_pre1-r3 \
  git==2.30.2-r0 \
  linux-headers==5.7.8-r0 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  libusb==1.0.24-r1 \
  libusb-dev==1.0.24-r1 \
  libxml2==2.9.10-r7 \
  libxml2-dev==2.9.10-r7 \
  libxslt==1.1.34-r0 \
  libxslt-dev==1.1.34-r0 \
  musl-dev==1.2.2-r1 \
  openssl==1.1.1k-r0 \
  openssl-dev==1.1.1k-r0 \
  python3-dev==3.8.10-r0 \
  rust==1.47.0-r2 \
  cargo==1.47.0-r2 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install --no-cache-dir git+https://github.com/MediaKraken/phue \
  && rm requirements.txt \
  && apk del \
  cargo \
  eudev-dev \
  gcc \
  git \
  libffi-dev \
  libusb-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  openssl-dev \
  python3-dev

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
