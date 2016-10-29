# Download base image
FROM alpine:3.4

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image hosts the postgresql database"

# Update Software repository
RUN apk add --update \
  postgresql \
  postgresql-contrib \
  postgresql-client

USER postgres

#ENV PATH /usr/lib/postgresql/9.5/bin:$PATH
#ENV PGDATA /var/lib/postgresql/data

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

EXPOSE 5432
CMD ["postgres"]
