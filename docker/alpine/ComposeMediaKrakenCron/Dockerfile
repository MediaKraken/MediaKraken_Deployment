# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the cron app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# had to go back to update instead of no-cache......throws errors
RUN sed -i "s/dl-2.cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  alpine-sdk \
  python3-dev \
  linux-headers \
  musl-dev \
  py3-psycopg2 \
  py3-psutil \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
  alpine-sdk \
  python3-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  && rm -rf /var/cache/apk/* \
  && rm requirements.txt

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
