# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image downloads and maintains all metadata"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-2.cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  ca-certificates \
  cifs-utils \
  nfs-utils \
  gcc \
  linux-headers \
  musl-dev \
  python3-dev \
  libffi-dev \
  libxslt-dev \
  libxml2-dev \
  openrc \
  libressl-dev \
  libarchive \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del gcc linux-headers musl-dev python3-dev \
  && rm requirements.txt \
  && apk add \
  py3-setuptools \
  py3-service_identity \
  && rc-update add netmount \
  && rc-update add rpcbind
#  && pip3 install -e git+https://github.com/agonzalezro/python-opensubtitles#egg=python-opensubtitles #TODO removed for now

RUN mkdir /mediakraken/cache
COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
