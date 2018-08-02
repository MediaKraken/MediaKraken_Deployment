FROM alpine:3.8

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update ca-certificates \
  opensmtpd && \
  #set up virtual mail system user
  addgroup -S vmail && \
  adduser -S -h /var/vmail -g 'Virtual Mail' -s /sbin/nologin -G vmail vmail \
  && rm -rf /var/cache/apk/*

VOLUME ["/etc/smtpd", "/var/vmail"]
EXPOSE 25 587
ENTRYPOINT ["/usr/sbin/smtpd"]
CMD ["-d"]
