FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./sites-available/* /etc/nginx/sites-available/
COPY ./conf.d /etc/nginx/conf.d
COPY ./ssl /etc/nginx/ssl

RUN ls -la /etc/nginx/ssl
