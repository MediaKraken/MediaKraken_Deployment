FROM logstash

MAINTAINER Daniel Ibáñez Fernández <daniel.ibanez@softonic.com>

ADD ./docker/logstash/config /config-dir

COPY ./docker/logstash/patterns/ /etc/logstash/patterns/

CMD ["-f","/config-dir/logstash.conf"]
