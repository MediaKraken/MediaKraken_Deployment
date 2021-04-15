#!/bin/bash

. /autopause/autopause-fcns.sh

. ${SCRIPTS:-/}start-utils


autopause_error_loop() {
  logAutopause "Available interfaces within the docker container:"
  INTERFACES=$(echo /sys/class/net/*)
  INTERFACES=${INTERFACES//\/sys\/class\/net\//}
  logAutopause "  $INTERFACES"
  logAutopause "Please set the environment variable AUTOPAUSE_KNOCK_INTERFACE to the interface that handles incoming connections."
  logAutopause "If unsure which interface to choose, run the ifconfig command in the container."
  logAutopause "Autopause failed to initialize. This log entry will be printed every 30 minutes."
  while :
  do
    sleep 1800
    logAutopause "Autopause failed to initialize."
  done
}

# wait for java process to be started
while :
do
  if java_process_exists ; then
    break
  fi
  sleep 0.1
done

# check for interface existence
if [[ -z "$AUTOPAUSE_KNOCK_INTERFACE" ]] ; then
  logAutopause "AUTOPAUSE_KNOCK_INTERFACE variable must not be empty!"
  autopause_error_loop
fi
if ! [[ -d "/sys/class/net/$AUTOPAUSE_KNOCK_INTERFACE" ]] ; then
  logAutopause "Selected interface \"$AUTOPAUSE_KNOCK_INTERFACE\" does not exist!"
  autopause_error_loop
fi

sudo /usr/sbin/knockd -c /tmp/knockd-config.cfg -d -i "$AUTOPAUSE_KNOCK_INTERFACE"
if [ $? -ne 0 ] ; then
  logAutopause "Failed to start knockd daemon."
  logAutopause "Probable cause: Unable to attach to interface \"$AUTOPAUSE_KNOCK_INTERFACE\"."
  autopause_error_loop
fi

STATE=INIT

while :
do
  case X$STATE in
  XINIT)
    # Server startup
    if mc_server_listening ; then
      TIME_THRESH=$(($(current_uptime)+$AUTOPAUSE_TIMEOUT_INIT))
      logAutopause "MC Server listening for connections - stopping in $AUTOPAUSE_TIMEOUT_INIT seconds"
      STATE=K
    fi
    ;;
  XK)
    # Knocked
    if java_clients_connected ; then
      logAutopause "Client connected - waiting for disconnect"
      STATE=E
    else
      if [[ $(current_uptime) -ge $TIME_THRESH ]] ; then
        logAutopause "No client connected since startup / knocked - stopping"
        /autopause/pause.sh
        STATE=S
      fi
    fi
    ;;
  XE)
    # Established
    if ! java_clients_connected ; then
      TIME_THRESH=$(($(current_uptime)+$AUTOPAUSE_TIMEOUT_EST))
      logAutopause "All clients disconnected - stopping in $AUTOPAUSE_TIMEOUT_EST seconds"
      STATE=I
    fi
    ;;
  XI)
    # Idle
    if java_clients_connected ; then
      logAutopause "Client reconnected - waiting for disconnect"
      STATE=E
    else
      if [[ $(current_uptime) -ge $TIME_THRESH ]] ; then
        logAutopause "No client reconnected - stopping"
        /autopause/pause.sh
        STATE=S
      fi
    fi
    ;;
  XS)
    # Stopped
    if rcon_client_exists ; then
      /autopause/resume.sh
    fi
    if java_running ; then
      if java_clients_connected ; then
        logAutopause "Client connected - waiting for disconnect"
        STATE=E
      else
        TIME_THRESH=$(($(current_uptime)+$AUTOPAUSE_TIMEOUT_KN))
        logAutopause "Server was knocked - waiting for clients or timeout"
        STATE=K
      fi
    fi
    ;;
  *)
    logAutopause "Error: invalid state: $STATE"
    ;;
  esac
  if [[ "$STATE" == "S" ]] ; then
    # before rcon times out
    sleep 2
  else
    sleep $AUTOPAUSE_PERIOD
  fi
done
