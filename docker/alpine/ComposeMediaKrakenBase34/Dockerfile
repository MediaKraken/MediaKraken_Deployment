# Download base image
FROM alpine:3.4

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken

WORKDIR /mediakraken

RUN apk add --update \
  python \
  py-pip \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/*

CMD ["/bin/ash"]
