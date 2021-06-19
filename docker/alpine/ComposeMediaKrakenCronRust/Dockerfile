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
FROM scratch

# Import from builder.
COPY --from=cargo-build /etc/passwd /etc/passwd
COPY --from=cargo-build /etc/group /etc/group

WORKDIR /myapp

# Copy our build
COPY --from=cargo-build /myapp/target/x86_64-unknown-linux-musl/release/myapp ./

# Use an unprivileged user.
USER myapp:myapp

CMD ["/myapp/myapp"]
