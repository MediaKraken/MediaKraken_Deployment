# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase38py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the hardware app"

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
  linux-headers \
  libffi-dev \
  libusb-dev \
  libxml2-dev \
  libxslt-dev \
  musl-dev \
  openssl-dev \
  python \
  python3-dev \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install git+https://github.com/MediaKraken/phue \
  && rm requirements.txt \
  && apk del \
  gcc \
  git \
  linux-headers \
  musl-dev \
  python3-dev

COPY wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
