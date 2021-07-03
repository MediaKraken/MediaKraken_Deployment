# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the downloader app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken/downloads

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apk add --no-cache \
  gcc==10.2.1_pre1-r3 \
  git==2.30.2-r0 \
  libxml2==2.9.10-r7 \
  libxml2-dev==2.9.10-r7 \
  linux-headers==5.7.8-r0 \
  musl-dev==1.2.2-r1 \
  py3-apache-libcloud==3.3.0-r0 \
  py3-psycopg2==2.8.6-r0 \
  python3-dev==3.8.10-r0 \
  xmlsec-dev==1.2.31-r0 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install --no-cache-dir -e git+https://github.com/MediaKraken-Dep/dosage#egg=dosage \
  && apk del \
  gcc \
  git \
  libxml2-dev \
  python3-dev \
  && rm requirements.txt

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
