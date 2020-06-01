# nginx-php-mysql

## Secrets
```
# parameters to connect to droplet per ssh
DC_HOST
DC_PORT
DC_USER
DC_KEY

# certificates to support https
SERVER_PEM
SERVER_KEY

# php mysql config
PHP_PARAMS

# phpmyadmin abs uri
PMA_ABSOLUTE_URI

# basic auth before opening site
SITE_AUTH_A
SITE_AUTH_B

# mysql params
MYSQL_INIT
MYSQL_TEST
MYSQL_ROOT_PASSWORD
MYSQL_HOST
```

## Install

### Docker
[Docker on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
After that, allow docker run without sudo and add allowed users to docker group
```
# create user
# sudo user, ref. https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart
sudo adduser github



```