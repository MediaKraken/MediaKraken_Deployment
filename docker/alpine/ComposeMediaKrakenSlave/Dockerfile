# Download base image
FROM mediakraken/mkbaseffmpeg

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apk add --update \
  openssl-dev \
  python \
  cifs-utils \
  nfs-utils \
  bash \
  postgresql-client \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  postgresql-dev \
  py-pip \
  python-dev \
  openrc \
  && pip install -r requirements.txt \
  && apk del \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  postgresql-dev \
  py-pip \
  python-dev \
  && apk add \
  py-setuptools \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/* \
  && rc-update add netmount \
  && rc-update add rpcbind

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
