FROM php:7.4-fpm

RUN apt-get update && apt-get install -y git zip unzip
RUN docker-php-ext-install mysqli pdo pdo_mysql

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
## for each project
# install vendors
#WORKDIR /var/www/html/web1
#RUN composer install --no-progress --no-suggest --no-interaction --prefer-dist --optimize-autoloader
# install vendors
#WORKDIR /var/www/html/web2
#RUN composer install --no-progress --no-suggest --no-interaction --prefer-dist --optimize-autoloader
# ...

RUN usermod -u 1000 www-data

COPY ./php.ini /usr/local/etc/php/conf.d/php.ini

WORKDIR /var/www/html

EXPOSE 9000