FROM logstash

MAINTAINER Daniel Ibáñez Fernández <daniel.ibanez@softonic.com>

ADD config /config-dir

COPY patterns/ /etc/logstash/patterns/

CMD ["-f","/config-dir/logstash.conf"]
