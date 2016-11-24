FROM debian:jessie

MAINTAINER Pierre-Antoine 'ZHAJOR' Tible <antoinetible@gmail.com>

RUN apt-get update \
  && apt-get -y install apache2 libapache2-mod-php5 php5 php5-pgsql wget unzip \
  && apt-get clean

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV PORT=5432
ENV HOST=mkdatabase

WORKDIR /var/www/html

RUN ln -sf /dev/stdout /var/log/apache2/access.log \
  && ln -sf /dev/stdout /var/log/apache2/error.log \
  && chown -R www-data:www-data /var/log/apache2 /var/www/html \
  && wget https://github.com/phppgadmin/phppgadmin/archive/master.zip \
  && rm /var/www/html/index.html && unzip /var/www/html/master.zip \
  && cp -R phppgadmin-master/* . && rm -r phppgadmin-master \
  && rm /var/www/html/master.zip \
  && rm -rf /var/lib/apt/lists/*

ADD config.inc.php /var/www/html/conf/config.inc.php
ADD wait-for-it-bash.sh /var/www/html
ADD run.sh /run.sh

RUN chmod -v +x /run.sh

EXPOSE 80

CMD ["/run.sh"]
