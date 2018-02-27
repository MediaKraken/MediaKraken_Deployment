FROM buildpack-deps:xenial-scm

# Versions of Nginx and nginx-rtmp-module to use
ENV NGINX_VERSION nginx-1.13.0
ENV NGINX_RTMP_MODULE_VERSION 1.1.11
ENV NGINX_VOD_MODULE_VERSION 1.16
ENV FFMPEG_VERSION 3.3

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    openssl \
    autoconf \
    automake \
    build-essential \
    libssl-dev \
    libass-dev \
    libfreetype6-dev \
    libtheora-dev \
    libtool \
    libvorbis-dev \
    cmake \
    mercurial \
    pkg-config \
    texinfo \
    yasm \
    libx264-dev \
    libx265-dev \
    libmp3lame-dev \
    libopus-dev \
    libvpx-dev \
    librtmp-dev \
    libpcre3 \
    libpcre3-dev \
    libfdk-aac-dev \
    vim \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Download and decompress Nginx
RUN mkdir -p /tmp/build/nginx && \
    cd /tmp/build/nginx && \
    wget -O ${NGINX_VERSION}.tar.gz https://nginx.org/download/${NGINX_VERSION}.tar.gz && \
    tar -zxf ${NGINX_VERSION}.tar.gz

# Download and decompress RTMP module
RUN mkdir -p /tmp/build/nginx-rtmp-module && \
    cd /tmp/build/nginx-rtmp-module && \
    wget -O nginx-rtmp-module-${NGINX_RTMP_MODULE_VERSION}.tar.gz https://github.com/arut/nginx-rtmp-module/archive/v${NGINX_RTMP_MODULE_VERSION}.tar.gz && \
    tar -zxf nginx-rtmp-module-${NGINX_RTMP_MODULE_VERSION}.tar.gz

# Download and decompress VOD module
RUN mkdir -p /tmp/build/nginx-vod-module && \
    cd /tmp/build/nginx-vod-module && \
    wget -O nginx-vod-module-${NGINX_VOD_MODULE_VERSION}.tar.gz https://github.com/kaltura/nginx-vod-module/archive/${NGINX_VOD_MODULE_VERSION}.tar.gz && \
    tar -zxf nginx-vod-module-${NGINX_VOD_MODULE_VERSION}.tar.gz

# Add nginx user and group
RUN addgroup --system nginx && \
    adduser --system --home /var/cache/nginx --disabled-password --ingroup nginx nginx

# Build and install Nginx
RUN cd /tmp/build/nginx/${NGINX_VERSION} && \
    ./configure \
    --add-module=/tmp/build/nginx-rtmp-module/nginx-rtmp-module-${NGINX_RTMP_MODULE_VERSION} \
    --add-module=/tmp/build/nginx-vod-module/nginx-vod-module-${NGINX_VOD_MODULE_VERSION} \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-file-aio \
    --with-threads \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-debug \
    --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' \
    --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie' && \
    make -j $(getconf _NPROCESSORS_ONLN) && \
    make install && \
    mkdir /var/lock/nginx && \
    rm -rf /tmp/build

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Get ffmpeg source.
RUN cd /tmp/ && \
 wget http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
 tar zxf ffmpeg-${FFMPEG_VERSION}.tar.gz && rm ffmpeg-${FFMPEG_VERSION}.tar.gz

# Compile ffmpeg.
RUN cd /tmp/ffmpeg-${FFMPEG_VERSION} && \
  ./configure \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-libfreetype \
  --enable-openssl \
  --enable-libvpx \
  --enable-nonfree && \
  make -j && \
  make install && \
  make distclean

# Set up config file
COPY nginx.conf.webcam /etc/nginx/nginx.conf

EXPOSE 8080
EXPOSE 1935

STOPSIGNAL SIGQUIT

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
#CMD ["nginx", "-g", "daemon off;"]


