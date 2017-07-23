# Download base image
FROM mediakraken/mkbaseffmpegnvidiadebian

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

# don't create /mediakraken as it's in the base image

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apt-get update \
  && apt-get install \
  python \
  cifs-utils \
  nfs-utils \
  bash \
  postgresql-client \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  net-snmp \
  net-snmp-dev \
  py-pip \
  python-dev \
  openrc \
  && pip install -r requirements.txt \
  && apk del \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  net-snmp-dev \
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
