# Download base image
FROM alpine:3.8

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken

WORKDIR /mediakraken

# pip3 is installed with python3
RUN apk add --update \
  python3 \
  && pip3 install --upgrade pip \
  && pip3 install -r requirements.txt \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/*

CMD ["/bin/ash"]
