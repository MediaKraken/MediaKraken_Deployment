FROM alpine:3.13.5

RUN addgroup -g 1000 myapp \
  && adduser -D -s /bin/sh -u 1000 -G myapp myapp

WORKDIR /home/myapp/bin/

COPY target/x86_64-unknown-linux-musl/release/myapp .

RUN chown myapp:myapp myapp

USER myapp

CMD ["./myapp"]