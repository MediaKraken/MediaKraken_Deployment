#!/bin/bash
# Starts odyssey
/etc/init.d/syslog-ng start
echo "Starting odyssey"
/usr/local/bin/odyssey /usr/local/bin/odyssey.conf && tail -f /var/log/odyssey.log
