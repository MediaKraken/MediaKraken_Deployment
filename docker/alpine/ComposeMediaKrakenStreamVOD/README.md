# nginx-rtmp-vod-ffmpeg
Simple RTMP server that stream /dev/video0 
## setup
#### docker-compose
`docker-compose up`
#### docker
* `docker build . -t nginx-rtmp-vod-ffmpeg`
* `docker run -it --rm -p 1935:1935 --device=/dev/video0:/dev/video0 nginx-rtmp-vod-ffmpeg`
## versions
* NGINX_VERSION nginx-1.13.0
* NGINX_RTMP_MODULE_VERSION 1.1.11
* NGINX_VOD_MODULE_VERSION 1.16
* FFMPEG_VERSION 3.3


