FROM debian:jessie

MAINTAINER Pierre-Antoine 'ZHAJOR' Tible <antoinetible@gmail.com>

RUN apt-get update
RUN apt-get -y install apache2 libapache2-mod-php5 php5 php5-pgsql wget unzip
RUN apt-get clean

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV PORT=5432
ENV HOST=database

RUN ln -sf /dev/stdout /var/log/apache2/access.log
RUN ln -sf /dev/stdout /var/log/apache2/error.log

RUN chown -R www-data:www-data /var/log/apache2 /var/www/html

WORKDIR /var/www/html
RUN wget https://github.com/phppgadmin/phppgadmin/archive/master.zip
RUN rm /var/www/html/index.html && unzip /var/www/html/master.zip
RUN cp -R phppgadmin-master/* . && rm -r phppgadmin-master

ADD config.inc.php /var/www/html/conf/config.inc.php

ADD run.sh /run.sh
RUN chmod -v +x /run.sh

EXPOSE 80

CMD ["/run.sh"]
