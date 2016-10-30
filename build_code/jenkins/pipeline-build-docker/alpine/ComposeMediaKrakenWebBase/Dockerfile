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
  gcc \
  py-pip \
  && pip install -r requirements.txt \
  && del gcc \
  py-pip
  && rm requirements.txt

