# Download base image
FROM mediakraken/mkbaseffmpeg:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the ripper app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN apk add --no-cache \
  abcde \
  openjdk8-jre-base \
  python3

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
