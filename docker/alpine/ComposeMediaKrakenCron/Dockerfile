# Download base image
FROM mediakraken/mkbase38py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the cron app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  alpine-sdk \
  python3-dev \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk add --no-cache \
  linux-headers \
  musl-dev \
  py3-psycopg2 \
  py3-psutil \
  && apk del \
  alpine-sdk \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  && rm requirements.txt

COPY wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
