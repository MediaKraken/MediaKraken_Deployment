# FFmpeg
FFmpeg Development Image for H.264-Processing (e.g. RTMP, HLS)

* Alipne Linux (3.6)
* FFmpeg
* Docker-Images for AMD64, ARMHF (e.g. Raspberry-Pi) and ARM64 (e.g. Pine64)

```sh
./configure
    --enable-nonfree
    --enable-gpl
    --enable-version3
    --enable-avresample
    --enable-libmp3lame
    --enable-libx264
    --enable-openssl
    --enable-postproc
    --enable-small
    --enable-libfdk_aac
    --enable-shared
    --disable-debug
    --disable-doc
    --disable-static
    --disable-ffserver
```

## Published Images

* `3.3.3`, `3.3`, `3` (docker pull `datarhei/ffmpeg:3.3`)
* `3.3.3-armhf`, `3.3-armhf`, `3-armhf` (docker pull `datarhei/ffmpeg:3.3-armhf`)
* `3.3.3-arm64`, `3.3-arm64`, `3-arm64` (docker pull `datarhei/ffmpeg:3.3-arm64`)
* `3.2.7`, `3.2` (docker pull `datarhei/ffmpeg:3.2`)
* `3.2.7-armhf`, `3.2-armhf` (docker pull `datarhei/ffmpeg:3.2-armhf`)
* `3.2.7-arm64`, `3.2-arm64` (docker pull `datarhei/ffmpeg:3.2-arm64`)
* `3.1.10`, `3.1` (docker pull `datarhei/ffmpeg:3.1`)
* `3.1.10-armhf`, `3.1-armhf` (docker pull `datarhei/ffmpeg:3.1-armhf`)
* `3.1.10-arm64`, `3.1-arm64` (docker pull `datarhei/ffmpeg:3.1-arm64`)
* `3.0.9`, `3.0` (docker pull `datarhei/ffmpeg:3.0`)
* `3.0.9-armhf`, `3.0-armhf` (docker pull `datarhei/ffmpeg:3.0-armhf`)
* `3.0.9-arm64`, `3.0-arm64` (docker pull `datarhei/ffmpeg:3.0-arm64`)
* `2.8.12`, `2.8`, `2` (docker pull `datarhei/ffmpeg:2.8`)
* `2.8.12-armhf`, `2.8-armhf`, `2-armhf` (docker pull `datarhei/ffmpeg:2.8-armhf`) 
* `2.8.12-arm64`, `2.8-arm64`, `2-arm64` (docker pull `datarhei/ffmpeg:2.8-arm64`) 
