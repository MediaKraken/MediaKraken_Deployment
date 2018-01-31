# Download base image
FROM alpine:3.7

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN apk add --update \
  python3 \
  && rm -rf /var/cache/apk/*

CMD ["/bin/ash"]
