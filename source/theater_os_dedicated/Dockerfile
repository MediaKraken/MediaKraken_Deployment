FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    gcc make git unzip wget xz-utils \
  && rm -rf /var/lib/apt/lists/*
  && git clone https://github.com/LibreELEC/LibreELEC.tv.git
  && cd LibreELEC.tv
  && git checkout 8.2.5

PROJECT=Generic ARCH=x86_64
PROJECT=Generic ARCH=x86_64 make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=RPi ARCH=arm
PROJECT=RPi ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=RPi2 ARCH=arm
PROJECT=RPi2 ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=Odroid_C2 ARCH=aarch64
PROJECT=Odroid_C2 ARCH=aarch64 make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=WeTek_Play ARCH=arm
PROJECT=WeTek_Play ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=WeTek_Play_2 ARCH=aarch64
PROJECT=WeTek_Play_2 ARCH=aarch64 make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=WeTek_Core ARCH=arm
PROJECT=WeTek_Core ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=WeTek_Hub ARCH=aarch64
PROJECT=WeTek_Hub ARCH=aarch64 make -j`getconf _NPROCESSORS_ONLN` image

PROJECT=imx6 ARCH=arm
PROJECT=imx6 ARCH=arm make image

PROJECT=Virtual ARCH=x86_64
PROJECT=Virtual ARCH=x86_64 make -j`getconf _NPROCESSORS_ONLN` image
