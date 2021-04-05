#!/bin/bash

. /start-utils

if [[ $( ps -a -o stat,comm | grep 'java' | awk '{ print $1 }') =~ ^S.*$ ]] ; then
  # save world
  rcon-cli save-all >/dev/null

  # wait until mc-monitor is no longer connected to the server
  while :
  do
    if [[ -z "$(netstat -nt | grep "127.0.0.1:$SERVER_PORT" | grep 'ESTABLISHED')" ]]; then
      break
    fi
    sleep 0.1
  done

  # finally pause the process
  logAutopauseAction "Pausing Java process"
  pkill -STOP java
fi
