# Download base image
FROM alpine:3.6

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN apk add --update \
  python \
  && rm -rf /var/cache/apk/*

CMD ["/bin/ash"]
