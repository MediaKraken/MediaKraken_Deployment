FROM rust:1.53.0 as cargo-build

RUN rustup target add x86_64-unknown-linux-musl
RUN apt update && apt install -y musl-tools musl-dev
RUN update-ca-certificates

# Create appuser
ENV USER=myapp
ENV UID=10001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

WORKDIR /myapp

COPY ./ .

RUN cargo build --target x86_64-unknown-linux-musl --release

####################################################################################################
## Final image
####################################################################################################
FROM busybox:1.33.1-uclibc
RUN wget -O /wait https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait &&\
    chmod +x /wait
# Import from builder.
COPY --from=cargo-build /etc/passwd /etc/passwd
COPY --from=cargo-build /etc/group /etc/group
COPY --from=cargo-build /bin/sh /sh

WORKDIR /myapp

# Copy our build
COPY --from=cargo-build /myapp/target/x86_64-unknown-linux-musl/release/myapp ./

# Use an unprivileged user.
USER myapp:myapp
