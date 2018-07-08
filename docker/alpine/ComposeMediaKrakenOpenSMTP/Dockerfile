FROM alpine:3.8

RUN apk add --no-cache ca-certificates
RUN apk add --no-cache opensmtpd && \
	# set up virtual mail system user
	addgroup -S vmail && \
	adduser -S -h /var/vmail -g 'Virtual Mail' -s /sbin/nologin -G vmail vmail

VOLUME ["/etc/smtpd", "/var/vmail"]
EXPOSE 25 587
ENTRYPOINT ["/usr/sbin/smtpd"]
CMD ["-d"]
