# Download base image
FROM  mediakraken/mkbaseffmpeg:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the dms app"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apk add --update \
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
  && pip3 install pycurl \
  && pip3 install -r requirements.txt \
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
  && rm -rf /var/cache/apk/* \
  && rm requirements.txt \

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
