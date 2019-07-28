# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase38py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image scans for new hardware devices"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  alpine-sdk \
  gcc \
  git \
  libhdhomerun \
  linux-headers \
  musl-dev \
  py3-requests \
  py3-setuptools \
  python3-dev \
  && git clone https://github.com/MediaKraken/PyHdHomeRun \
  && cd PyHdHomeRun \
  && python3 setup.py install \
  && cd .. \
  && rm -R PyHdHomeRun \
  && git clone https://github.com/MediaKraken/phue \
  && cd phue \
  && python3 setup.py install \
  && cd .. \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del alpine-sdk \
  git \
  python3-dev \
  linux-headers \
  && rm -rf phue \
  && rm requirements.txt

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
