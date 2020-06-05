FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./sites-available/* /etc/nginx/sites-available/
COPY ./conf.d/credentials.conf /etc/nginx/conf.d/credentials.conf
COPY ./conf.d/wsites/* /etc/nginx/conf.d/
COPY ./ssl/wsites/* /etc/ssl/

RUN chmod -R 777 /etc/nginx/conf.d/
RUN chmod -R 777 /etc/ssl/

RUN ls -la /etc/nginx/conf.d/
RUN ls -la /etc/ssl/

