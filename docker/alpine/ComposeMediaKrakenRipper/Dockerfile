# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_ffmpeg:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the ripper app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN apk add --no-cache \
  abcde==2.9.3-r0 \
  openjdk8-jre-base==8.275.01-r0 \
  python3-dev==3.8.10-r0

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
