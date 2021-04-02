# Download base image
FROM  th-registry-1.beaverbay.local:5000/mediakraken/mkbaseffmpeg:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the dms app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  go \
  go get github.com/anacrolix/dms \
  cifs-utils==6.12-r0 \
  curl \
  curl-dev \
  nfs-utils==2.5.2-r0 \
  postgresql-client \
  openssl \
  alpine-sdk \
  libffi \
  libffi-dev \
  openldap-dev \
  jpeg \
  jpeg-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers==5.7.8-r0 \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  portaudio-dev \
  postgresql-dev \
  python3-dev \
  openrc==0.42.1-r19 \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && apk del \
  alpine-sdk \
  curl-dev \
  jpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  postgresql-dev \
  python3-dev \
  && apk add \
  py-setuptools \
  && rm requirements.txt \

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
