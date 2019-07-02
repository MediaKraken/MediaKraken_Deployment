# Download base image
FROM mediakraken/mkbase38py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the downloader app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken/downloads

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  gcc \
  git \
  libxml2-dev \
  linux-headers \
  musl-dev \
  py3-libcloud \
  py3-psycopg2 \
  python3-dev \
  xmlsec-dev \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install -e git+https://github.com/MediaKraken-Dep/dosage#egg=dosage \
  && apk del \
  gcc \
  git \
  && rm -rf /var/cache/apk/* \
  && rm requirements.txt

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
