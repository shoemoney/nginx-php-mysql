FROM php:7.4-fpm

RUN apt-get update && apt-get install -y git zip unzip
RUN docker-php-ext-install mysqli pdo pdo_mysql

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN useradd -m -G root github
RUN chmod -R 777 /usr/local/etc/php
RUN chmod -R 777 /var/www/html

COPY ./php.ini /usr/local/etc/php/conf.d/php.ini

WORKDIR /var/www/html

EXPOSE 9000