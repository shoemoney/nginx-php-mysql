FROM phpmyadmin/phpmyadmin:latest

RUN useradd -m -G root github
RUN chmod -R 777 /usr/local/etc/php
RUN chmod -R 777 /var/www/html
RUN chmod -R 777 /etc/phpmyadmin/

WORKDIR /var/www/html

EXPOSE 8080