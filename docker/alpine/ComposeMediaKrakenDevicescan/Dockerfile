# Download base image
FROM mediakraken/mkbase37py3

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image scans for new hardware devices"

WORKDIR /mediakraken

# add hdhomerun lib to install
ADD PyHdHomeRun /mediakraken/PyHdHomeRun
ADD libhdhomerun /mediakraken/libhdhomerun
ADD libhdhomerun_python /mediakraken/libhdhomerun_python

# Update repository and install packages
RUN apk add --update \
  alpine-sdk \
  py3-requests \
  py3-setuptools \
  python3-dev \
  && cd libhdhomerun \
  && make -j`getconf _NPROCESSORS_ONLN` \
  && cd .. \
  && mv ./libhdhomerun/hdhomerun_config . \
  && mv ./libhdhomerun/libhdhomerun.so /usr/lib/. \
  && mv libhdhomerun /usr/include/. \
  && cd PyHdHomeRun \
  && python setup.py install \
  && cd .. \
  && rm -R PyHdHomeRun \
  && cd libhdhomerun_python \
  && python setup.py install \
  && cd .. \
  && rm -R libhdhomerun_python \
  && rm -R /usr/include/libhdhomerun \
  && apk del alpine-sdk \
  python3-dev \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]



