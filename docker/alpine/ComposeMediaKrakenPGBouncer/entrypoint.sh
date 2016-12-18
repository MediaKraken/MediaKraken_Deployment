#!/bin/sh
CLIENT_IDLE_TIMEOUT=${CLIENT_IDLE_TIMEOUT:-0.0}
IGNORE_STARTUP_PARAMETERS=${IGNORE_STARTUP_PARAMETERS:-"extra_float_digits"}
DEFAULT_POOL_SIZE=${DEFAULT_POOL_SIZE:-90}
MAX_CLIENT_CONN=${MAX_CLIENT_CONN:-500}
SERVER_RESET_QUERY=${SERVER_RESET_QUERY:-"DISCARD ALL"}
POOL_MODE=${POOL_MODE:-transaction}
LISTEN_PORT=${LISTEN_PORT:-5432}

sed -i "s/\${DB}/${DB}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${HOST}/${HOST}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${PORT}/${PORT}/" /etc/pgbouncer/pgbouncer.ini

sed -i "s/\${CLIENT_IDLE_TIMEOUT}/${CLIENT_IDLE_TIMEOUT}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${IGNORE_STARTUP_PARAMETERS}/${IGNORE_STARTUP_PARAMETERS}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${DEFAULT_POOL_SIZE}/${DEFAULT_POOL_SIZE}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${MAX_CLIENT_CONN}/${MAX_CLIENT_CONN}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${SERVER_RESET_QUERY}/${SERVER_RESET_QUERY}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${POOL_MODE}/${POOL_MODE}/" /etc/pgbouncer/pgbouncer.ini
sed -i "s/\${LISTEN_PORT}/${LISTEN_PORT}/" /etc/pgbouncer/pgbouncer.ini

echo "\"${USER}\" \"${PASSWORD}\"" > /etc/pgbouncer/userlist.txt

exec /usr/local/bin/pgbouncer $@
