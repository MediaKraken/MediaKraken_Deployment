# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image scans for new hardware devices"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --no-cache \
  alpine-sdk==1.0-r0 \
  gcc==10.2.1_pre1-r3 \
  git==2.30.2-r0 \
  libhdhomerun==20200225-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r1 \
  py3-requests==2.25.1-r1 \
  py3-setuptools==51.3.3-r0 \
  python3-dev==3.8.10-r0 \
  && git clone https://github.com/MediaKraken/PyHdHomeRun \
  && cd PyHdHomeRun \
  && python3 setup.py install \
  && cd .. \
  && rm -R PyHdHomeRun \
  && git clone https://github.com/MediaKraken/phue \
  && cd phue \
  && python3 setup.py install \
  && cd .. \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del alpine-sdk \
  git \
  python3-dev \
  linux-headers \
  && rm -rf phue \
  && rm requirements.txt

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
