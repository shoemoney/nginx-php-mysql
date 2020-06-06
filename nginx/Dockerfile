FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./sites-available/* /etc/nginx/sites-available/
COPY ./conf.d/credentials.conf /etc/nginx/conf.d/credentials.conf
COPY ./conf.d/wsites/* /etc/nginx/conf.d/passwd/
COPY ./ssl/wsites/* /etc/nginx/conf.d/certs/

RUN useradd -m -G root github
RUN groups github
RUN chmod -R 777 /etc

