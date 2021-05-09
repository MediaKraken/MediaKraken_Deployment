# Download base image
FROM mediakraken/mkbase_alpinepy3:dev2021_04

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the cron app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# had to go back to update instead of no-cache......throws errors
RUN apk add --no-cache \
  alpine-sdk==1.0-r0 \
  python3-dev==3.8.10-r0 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r0 \
  py3-psycopg2==2.8.6-r0 \
  py3-psutil==5.8.0-r0 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  alpine-sdk \
  python3-dev \
  linux-headers \
  musl-dev \
  && rm requirements.txt

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
