# https://github.com/brainsam/pgbouncer

FROM alpine:3.8

MAINTAINER brainsam@yandex.ru

ARG ALPMIRROR
ARG PIPMIRROR

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
        && apk --update add git build-base automake libtool m4 autoconf libevent-dev libressl-dev c-ares c-ares-dev py-docutils && \
	git clone https://github.com/pgbouncer/pgbouncer.git && \
	cd pgbouncer         && \
        git checkout tags/pgbouncer_1_8_1 && \
	git submodule init   && \
	git submodule update && \
	./autogen.sh         && \
	./configure --prefix=/usr/local --with-libevent=/usr/lib && \
	make -j`getconf _NPROCESSORS_ONLN` && make install && \
	apk del git build-base automake autoconf c-ares-dev libtool m4 && \
	rm -f /var/cache/apk/* \
        && cd .. && rm -Rf pgbouncer

ADD entrypoint.sh ./
ADD wait-for-it-ash.sh ./

ENTRYPOINT ["./entrypoint.sh"]

