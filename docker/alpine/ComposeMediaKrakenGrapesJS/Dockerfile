# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbasenode:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the GrapesJS app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  && npm install -g grapesjs \
  && rm -rf /var/cache/apk/* \
  && rm -r /root/.npm

CMD ["/bin/ash"]
