FROM alpine:edge
MAINTAINER George Kutsurua <g.kutsurua@gmail.com>

RUN apk update && \
    apk add c-ares-dev libevent openssl && \
    mkdir -p /var/log/pgbouncer /var/run/pgbouncer && \
    chown postgres:postgres /var/log/pgbouncer /var/run/pgbouncer

COPY bin/pgbouncer-1.7.2 /usr/local/bin/pgbouncer
COPY pgbouncer.ini /etc/pgbouncer/pgbouncer.ini
COPY entrypoint.sh /

ENV DB=database HOST=host PORT=5432 \
    CLIENT_IDLE_TIMEOUT=0.0 IGNORE_STARTUP_PARAMETERS="extra_float_digits" \
    DEFAULT_POOL_SIZE=90 MAX_CLIENT_CONN=500 SERVER_RESET_QUERY="DISCARD ALL" \
    POOL_MODE=transaction LISTEN_PORT=5432

EXPOSE $LISTEN_PORT

ENTRYPOINT ["/entrypoint.sh"]
CMD ["-u", "postgres", "/etc/pgbouncer/pgbouncer.ini"]