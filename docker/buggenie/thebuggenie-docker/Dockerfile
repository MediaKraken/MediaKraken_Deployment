FROM tutum/lamp

RUN apt-get update && apt-get -y install curl && \
    git clone -b 4.1.13 https://github.com/thebuggenie/thebuggenie /var/www/thebuggenie

WORKDIR /var/www/thebuggenie

RUN curl -sS https://getcomposer.org/installer | php

RUN apt-get update && apt-get -y install \
    php5-gd php5-curl php5-ldap nano

RUN php composer.phar install

ADD 000-default.conf /etc/apache2/sites-available/000-default.conf

COPY ru_RU.tar.gz /var/www/thebuggenie/ru_RU.tar.gz

RUN tar -zxvf ru_RU.tar.gz

ADD create_mysql_admin_user.sh /create_mysql_admin_user.sh

RUN chown -R www-data:www-data /var/www/thebuggenie && \
    chmod a+w /create_mysql_admin_user.sh

EXPOSE 80 

CMD ["/run.sh"]
