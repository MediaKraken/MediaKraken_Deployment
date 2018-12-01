# Download base image
FROM mediakraken/mkbase38py3

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image scans for new hardware devices"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
ADD requirements.txt /mediakraken

WORKDIR /mediakraken

# add hdhomerun lib to install
ADD PyHdHomeRun /mediakraken/PyHdHomeRun

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  alpine-sdk \
  git \
  libhdhomerun \
  py3-requests \
  py3-setuptools \
  python3-dev \
  && cd PyHdHomeRun \
  && python3 setup.py install \
  && cd .. \
  && rm -R PyHdHomeRun \
  && get https://github.com/MediaKraken/phue \
  && cd phue \
  && python3 setup.py install \
  && cd .. \
  && apk del alpine-sdk \
  git \
  python3-dev \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm -rf phue \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]

