#!/usr/bin/env bash

nginx -g "daemon off;" &

ffmpeg -input_format mjpeg -fpsprobesize 10 -fflags +genpts+igndts -f v4l2 -i /dev/video0 -c:v libx264 -crf 30 -preset:v ultrafast -bf 2 -qp 18 -an -tune zerolatency -f flv rtmp://127.0.0.1:1935/webcam/video0
