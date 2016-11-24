#!/bin/bash

rm /run/apache2/apache2.pid
exec /usr/sbin/apache2ctl -D FOREGROUND
