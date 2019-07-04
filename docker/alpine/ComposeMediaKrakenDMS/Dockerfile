# Download base image
FROM  mediakraken/mkbaseffmpeg:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the dms app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  go \
  go get github.com/anacrolix/dms \
  cifs-utils \
  curl-dev \
  nfs-utils \
  postgresql-client \
  openssl \
  alpine-sdk \
  libffi-dev \
  openldap-dev \
  jpeg-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  openldap-dev \
  portaudio-dev \
  postgresql-dev \
  python3-dev \
  openrc \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && apk del \
  alpine-sdk \
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
