FROM alpine:3.6

# Add build dependencies
RUN apk add --no-cache --virtual .build-deps \
        bzip2-dev \
        expat-dev \
        gcc \
        gdbm-dev \
        libc-dev \
        libffi-dev \
        linux-headers \
        make \
        ncurses-dev \
        openssl-dev \
        pax-utils \
        readline-dev \
        sqlite-dev \
        tar \
        tk \
        tk-dev \
        zlib-dev

# Download the source
ENV PYPY_VERSION 5.8.0

RUN set -ex; \
    apk add --no-cache wget; \
    wget -O --no-check-certificate https://bitbucket.org/pypy/pypy/downloads/pypy2-v${PYPY_VERSION}-src.tar.bz2; \
    mkdir -p /usr/src/pypy; \
    tar -xjC /usr/src/pypy --strip-components=1 -f pypy2-v${PYPY_VERSION}-src.tar.bz2; \
    rm pypy2-v${PYPY_VERSION}-src.tar.bz2; \
    apk del wget

WORKDIR /usr/src/pypy
