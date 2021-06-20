# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image downloads and maintains all metadata"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --no-cache \
  ca-certificates==20191127-r5 \
  cifs-utils==6.13-r0 \
  nfs-utils==2.5.2-r0 \
  gcc==10.2.1_pre1-r3 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r1 \
  python3-dev==3.8.10-r0 \
  libffi==3.3-r2 \
  libffi-dev==3.3-r2 \
  libxslt==1.1.34-r0 \
  libxslt-dev==1.1.34-r0 \
  libxml2==2.9.10-r7 \
  libxml2-dev==2.9.10-r7 \
  openrc==0.42.1-r20 \
  libressl==3.1.5-r0 \
  libressl-dev==3.1.5-r0 \
  libarchive==3.5.1-r0 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  gcc \
  libffi-dev \
  linux-headers \
  libxslt-dev \
  libxml2-dev \
  libressl-dev \
  musl-dev \
  python3-dev \
  && rm requirements.txt \
  && apk add --no-cache \
  py3-setuptools==51.3.3-r0 \
  py3-service_identity==18.1.0-r3 \
  && rc-update add netmount \
  && rc-update add rpcbind
#  && pip3 install -e git+https://github.com/agonzalezro/python-opensubtitles#egg=python-opensubtitles #TODO removed for now

RUN mkdir /mediakraken/cache
COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
