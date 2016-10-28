# Download base image
FROM alpine:3.4

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Update Software repository
RUN apk add --update postgresql-9.5.4-r0 postgresql-contrib-9.5.4-r0 postgresql-client-9.5.4-r0

ENV PATH /usr/lib/postgresql/9.5/bin:$PATH
ENV PGDATA /var/lib/postgresql/data
VOLUME /var/lib/postgresql/data

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432
CMD ["postgres"]
