FROM rust:1.51 as cargo-build

RUN apt-get update

RUN apt-get install musl-tools libssl-dev -y

RUN rustup target add x86_64-unknown-linux-musl

RUN docker run --rm -it -v "$(pwd)":/home/rust/src messense/rust-musl-cross:x86_64-musl cargo build --release

# ------------------------------------------------------------------------------
# Final Stage
# ------------------------------------------------------------------------------

FROM alpine:3.13.5

RUN addgroup -g 1000 myapp \
  && adduser -D -s /bin/sh -u 1000 -G myapp myapp

WORKDIR /home/myapp/bin/

COPY --from=cargo-build /usr/src/myapp/target/x86_64-unknown-linux-musl/release/myapp .

RUN chown myapp:myapp myapp

USER myapp

CMD ["./myapp"]