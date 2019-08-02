# https://github.com/yandex/odyssey/issues/36
FROM debian:stretch-slim as builder

WORKDIR /tmp/

RUN set -ex \
&& apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends \
build-essential \
cmake \
git \
libssl-dev \
&& git clone git://github.com/yandex/odyssey.git \
&& cd odyssey \
&& mkdir build \
&& cd build \
&& cmake -DCMAKE_BUILD_TYPE=Release .. \
&& make

FROM debian:stretch-slim
RUN set -ex \
&& apt-get update \
&& apt-get install -y --no-install-recommends libssl-dev syslog-ng \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY --from=builder /tmp/odyssey/build/sources/odyssey /usr/local/bin/
COPY odyssey.conf /usr/local/bin/
COPY start_odyssey.sh /usr/local/bin/
EXPOSE 6432
CMD ["/usr/local/bin/start_odyssey.sh"]
