FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./sites-available /etc/nginx/sites-available
COPY ./conf.d/credentials.conf /etc/nginx/conf.d/credentials.conf
COPY ./ssl /etc/ssl
