#!/bin/ash
set -e
TS3_DATABASE="/opt/teamspeak/ts3server.sqlitedb"
# Functions
sig_int () {
    echo "SIGINT received"
    kill -2 ${pid}
}

sig_term () {
    echo "SIGTERM received"
    kill -15 ${pid}
}

install_ts3() {
  echo "Installing Teamspeak version: ${TS3_VERSION}"
  mkdir -p /opt/teamspeak
  tar jxf /tmp/teamspeak.tar.bz2 -C /opt/teamspeak --strip-components=1
  rm -f /tmp/teamspeak.tar.bz2
  echo "Teamspeak version: ${TS3_VERSION} installed."
}

if [[ ! -e ${TS3_DATABASE} ]]; then
  install_ts3
fi

./opt/teamspeak/ts3server_minimal_runscript.sh $@ &
pid=$!
trap sig_int  INT
trap sig_term TERM

wait $pid
