FROM frolvlad/alpine-glibc:glibc-2.25
# Note that we should be using frolvlad/alpine-mono (see note below) but can't because
# glibc-2.26 requires a newer kernel than is available on a lot of hosts (old OpenVZ)

MAINTAINER Jason Rivers <docker@jasonrivers.co.uk>

ARG USER=windward
ARG GROUP=windward
ARG PUID=1000
ARG PGID=1000

ENV WINDWARD_SERVER_NAME="Windward Server" \
    WINDWARD_SERVER_WORLD="World" \
    WINDWARD_SERVER_PORT=5127 \
    WINDWARD_SERVER_PUBLIC=0

RUN apk --update --no-cache add curl unzip

# Note - This line taken from frolvlad/alpine-mono since we have to build it ourselves here
RUN apk add --no-cache --virtual=.build-dependencies wget ca-certificates tar xz && \
    wget "https://www.archlinux.org/packages/extra/x86_64/mono/download/" -O "/tmp/mono.pkg.tar.xz" && \
    tar -xJf "/tmp/mono.pkg.tar.xz" && \
    cert-sync /etc/ssl/certs/ca-certificates.crt && \
    apk del .build-dependencies && \
    rm /tmp/*

RUN mkdir -p /windward && \
    chmod ugo=rwx /windward && \
	addgroup -g $PGID -S $GROUP && \
	adduser -u $PUID -G $GROUP -s /bin/sh -SD $USER && \
    chown -R $USER:$GROUP /windward /home/windward && \
	ln -s /windward /home/windward/Windward
	
VOLUME /windward

EXPOSE $WINDWARD_SERVER_PORT

COPY ./windward.sh /

USER $USER

CMD ["/windward.sh"]
