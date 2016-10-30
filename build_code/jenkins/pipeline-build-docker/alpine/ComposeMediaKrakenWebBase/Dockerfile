# Download base image
FROM alpine:3.4 

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image holds the base image for web/flask"

RUN mkdir /mediakraken
# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  ack \
  gcc \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  nginx \
  py-cffi \
  py-pip \
  py-redis \
  python-dev \
  redis \
  && pip install -r requirements.txt \
  && apk del \
  gcc \
  musl-dev \
  linux-headers \
  py-pip \
  python-dev \
  && rm requirements.txt \
  && apk add \
  uwsgi-python \
  uwsgi-router_uwsgi \
  && cp /usr/lib/uwsgi/python_plugin.so /mediakraken/. \
  && rc-update add nginx \
  && rc-update add redis


