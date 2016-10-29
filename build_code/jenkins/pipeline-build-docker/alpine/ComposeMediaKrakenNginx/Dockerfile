FROM alpine:3.4

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image hosts static media via Nginx"

RUN apk --update add nginx ca-certificates

ADD nginx.conf /etc/nginx/nginx.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log

VOLUME ["/var/cache/nginx"]

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
