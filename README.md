# NGINX PHP PHPMYADMIN MYSQL COMPOSER


## Pre-Install

### Python 
[Install guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server)
```
sudo apt-get update && sudo apt-get -y upgrade

# check python version
python3 --version

# basic packages
sudo apt install -y python3-pip
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev

```

### User github
```
## allow ssh,
sudo nano /etc/ssh/sshd_config
# Update content, uncomment/add
-> Port 25000 # or any another port
-> PermitRootLogin no
-> AllowUsers github
-> PubkeyAuthentication yes
-> AuthorizedKeysFile	.ssh/authorized_keys .ssh/authorized_keys2
# generate sshd dir
sudo mkdir /var/run/sshd/
# restart ssh
sudo systemctl restart ssh
# restart server
shutdown -r now

## create user
# sudo user, ref. https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart
sudo adduser github
sudo usermod -aG root github
sudo usermod -aG sudo github
# generate key
cd ~
ssh-keygen
cat ~/.ssh/id_rsa > ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub
# copy ~/.ssh/id_rsa to local, save under ~/.ssh/github_xxx
# On local machine
chmod -R 600 ~/.ssh/github_xxx
# restart ssh
sudo systemctl restart ssh
# restart server
shutdown -r now
# check ssh
ssh github@ip -p 25000 -i ~/.ssh/github_xxx
```

**SSH**
```
ref. https://www.howtogeek.com/168119/fixing-warning-unprotected-private-key-file-on-linux/
su - github

ssh-keygen

# ~/.ssh/id_rsa for DC_KEY of github secret setting
cat ~/.ssh/id_rsa > ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub

su - root
sudo systemctl restart ssh
```

### Mysql client
```
sudo apt install mysql-client-core-8.0 # Ubuntu 20.04
```

### Docker
[Docker on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)

After that, allow docker run without sudo and add allowed users to docker group
```
## add to docker group
sudo usermod -aG docker github
# check group
groups github
# login to github
su - github
# check github in docker group
id -nG
# docker helps without sudo
docker --help

# rights for user
sudo chmod 777 -R /var/run
sudo chmod 777 -R /tmp
# ...

```

### Github-runner
ONLY when runner still not be deployed and should be deployed on such the server 

[Repo github-runner docker](https://github.com/cross-the-world/github-runner)

**Add** these env variables to "~/.profile" 
```
RUNNER_ORGANIZATION_URL=https://github.com/[organization name]
GITHUB_ACCESS_TOKEN=personal_token
RUNNER_REPLACE_EXISTING=True
```
**Run** 
```
source ~/.profile
```
**Deploy** github-runner on server with docker
```
docker run -it --name github-runner \
    -e RUNNER_NAME=github-runner \
    -e GITHUB_ACCESS_TOKEN=${GITHUB_ACCESS_TOKEN} \
    -e RUNNER_ORGANIZATION_URL=${RUNNER_ORGANIZATION_URL} \
    -e RUNNER_REPLACE_EXISTING=${RUNNER_REPLACE_EXISTING} \
    -v /var/run/docker.sock:/var/run/docker.sock \
    thuong/github-runner:latest
```
**Open** [https://github.com/organizations/name/settings/actions](https://github.com/organizations/name/settings/actions) 
and check whether runner is ready


## Secrets
For each repository [https://github.com/repository_url/settings/secrets](https://github.com/repository_url/settings/secrets), 
since free license can not extend secrets from organization.
```
## parameters to connect to server per ssh, scp
DC_HOST
DC_PORT
DC_USER
DC_KEY
# if not use ssh key then DC_PASS as secrets 
#DC_PASS

## certificates to support https
#written to ./nginx/ssl/wsites/[site].pem, mount to nginx-container /etc/nginx/ssl/*
#written to ./nginx/ssl/wsites/[site].key, mount to nginx-container /etc/nginx/ssl/*
SSL 

## php mysql config
# written to ./nginx/conf.d/credentials.conf, mount to nginx-container /etc/nginx/conf.d/
# where using as params under $_SERVER in php
PHP_PARAMS 

## phpmyadmin abs uri
PMA_ABSOLUTE_URI
# e.g. https://pma.xxx/ubuntu-s-4vcpu-8gb-sfo2-01

## basic auth before opening site
# written to ./nginx/conf.d/wsites/.[site]passwd, mount to nginx-container /etc/nginx/conf.d/
#using on loading site with basic auth
SITE_AUTH

## mysql params
# written to ./mysql/init/init.sql, mount to mysql-container /docker-entrypoint-initdb.d/
# initialize database and privilliges for sites A,B,...
MYSQL_INIT 
# written to ./mysql/init/test.sql, mount to mysql-container /docker-entrypoint-initdb.d/
# test whether sql script on triggered
MYSQL_TEST
# root pwd, e.g secret
MYSQL_ROOT_PASSWORD
# using to set container name of docker mysql and bind host to phpmyadmin
# e.g. mysql
MYSQL_HOST
```

##### DC_HOST
```
server_ip
```

##### DC_PORT
```
ssh_port, e.g. 25000
```

##### DC_USER
```
user, e.g. github
```

##### DC_KEY
e.g.
```
private_key, e.g. $server> cat ~/.ssh/id_rsa
```

##### DC_PASS
in case DC_PASS is not inuse 
```
xxx
```

##### SSL
cloudflare is used only when 
* SSLVerifyClient require
* SSLCACertificateFile /usr/local/apache2/conf/certs/cloudflare.pem

e.g. 
```json
{
  "cloudflare": {
    "pem": "-----BEGIN CERTIFICATE-----xxx-----END CERTIFICATE-----"
  },
  "domain1": {
    "key": "-----BEGIN PRIVATE KEY-----xxx-----END PRIVATE KEY-----",
    "pem": "-----BEGIN CERTIFICATE-----xxx-----END CERTIFICATE-----"
  },
  "domain2": {
    "key": "-----BEGIN PRIVATE KEY-----xxx-----END PRIVATE KEY-----",
    "pem": "-----BEGIN CERTIFICATE-----xxx-----END CERTIFICATE-----"
  },
  "...": {}
}
```

##### PHP_PARAMS
e.g.
```
# database credentials for web1
fastcgi_param web1 'mysql:a_db:a_user:a_passwd';

# database credentials for web1
fastcgi_param web2 'mysql:b_db:b_user:b_passwd';
``` 

##### PMA_ABSOLUTE_URI
e.g. consider ./apache/sites-available/pma.conf
```
http://pma.domain_name/server_name
```

##### SITE_AUTH
generate passowrd with htpasswd
```
# create user:htpasswd for user
htpasswd -n user
# output [user]:[htpasswd]
```

e.g. add such
```json
{
  "domain1": "[user]:[htpasswd]",
  "domain2": "[user]:[htpasswd]",
  "...": "..."
}
```

##### MYSQL_INIT
e.g.
```sql
CREATE DATABASE IF NOT EXISTS a_db;
CREATE USER 'a_user'@'%' IDENTIFIED BY 'a_passwd';
GRANT ALL PRIVILEGES ON a_db.* TO 'a_user'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS b_db;
CREATE USER 'b_user'@'%' IDENTIFIED BY 'b_passwd';
GRANT ALL PRIVILEGES ON b_db.* TO 'b_user'@'%';
FLUSH PRIVILEGES;

-- 'secret' = MYSQL_ROOT_PASSWORD
CREATE USER 'root'@'%' IDENTIFIED BY 'secret';
GRANT ALL ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
```

##### MYSQL_TEST
e.g.
```
#!/bin/bash
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "                          TEST                                  "
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```


## New site
for a NEW WEBSITE xxx

### Configuration
* Source code must be under "./www/xxx"
* Nginx proxy configuration "./nginx/sites-available/xxx.conf", ref."./nginx/sites-available/A.conf" (considering http/https)
    ```
      server {
        listen 80;
        listen [::]:80;
      
        # your domain
        server_name SITE_DOMAIN;
        # ROOT SOURCE, where to load the index.php
        root /var/www/html/xxx/public;
      
        index index.php index.html;
        error_log  /var/log/nginx/error.log;
        access_log /var/log/nginx/access.log;
      
        proxy_cache                     off;
      
        # Headers for client browser NOCACHE + CORS origin filter
        add_header 'Cache-Control' 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
        expires off;
        add_header    'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header    'Access-Control-Allow-Headers' 'Origin, X-Requested-With, Content-Type, Accept' always;
      
        location / {
          try_files $uri $uri/ =404;
          # Relate to e.g secret "SITE_AUTH_A"
          #auth_basic "Restricted Content";
          #auth_basic_user_file /etc/nginx/conf.d/.apasswd;
      
          # pass the PHP scripts to FastCGI server listening on docker php
          location ~* "\.php$" {
            #	include snippets/fastcgi-php.conf;      
            try_files $uri =404;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            # All php sources are routed to PHP container (container name php), port 9000
            fastcgi_pass php:9000;
            fastcgi_index index.php;
      
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            include /etc/nginx/conf.d/credentials.conf;
          }
        }    
      }
    ```
* Some credentials can be added to secret "PHP_PARAMS", e.g. mysql credential
    ```
    # database credentials for web1
    fastcgi_param web1 'mysql:a_db:a_user:a_passwd';
    
    # database credentials for web1
    fastcgi_param web2 'mysql:b_db:b_user:b_passwd';
  
    # ...
    ```
    * including it in proxy config under "./nginx/sites-available/xxx.conf"
        ```
        server {
          # ...
        
          location / {
            # ...
            # pass the PHP scripts to FastCGI server listening on docker php
            location ~* "\.php$" {
              # ...
      
              # here config is included, and mapped to $_SERVER of php
              include /etc/nginx/conf.d/credentials.conf;
            }
          }
        }
        ```
    * using it in source, e.g. under "./www/xxx/app/Config/Database.php"
        ```
        #load db string value of web1
        $this->db_string = $_SERVER['web1'];
        #parse it to array 4 elems, split by ":"
        $this->db_values = explode(":", $this->db_string, 4);
      
        $this->default['DSN'] = 'mysql:host='.$this->db_values[0].';port=3306;dbname='.$this->db_values[1];
        $this->default['hostname'] = $this->db_values[0];
        $this->default['username'] = $this->db_values[2];
        $this->default['password'] = $this->db_values[3];
        $this->default['database'] = $this->db_values[1];
        ```
* add a container in "docker-compose.yml" to generate dependencies for the site xxx, 
if the site xxx e.g. uses "composer" for such thing
    ```
    composer-xxx:
      build:
        context: ./composer
        dockerfile: Dockerfile
      container_name: composer-xxx
      #ensure the dependencies generated under the dedicted user, 
      #in this case "github"
      user: ${CURRENT_UID} 
      volumes:
        #the dependencies are generated to /app inside the container, 
        #but are mounted by the volumn outsite. 
        #It should be synced from inside to outside 
        #and used in nginx and php containers.
        - "./www/web2:/app" 
    ```


## Deploy 

### Manual for test
```
## add domain to localhost
# e.g. macos
sudo nano /etc/hosts
# Add these line and uncomment and save
#127.0.0.1       domain
#127.0.0.1       web1.domain
#127.0.0.1       web2.domain

## Goto source folder
cd [src folder]

## ref.src. "./docker-compose.yml"
# build images
docker-compose build --no-cache

# remove all deployed containters
docker-compose rm -fs

# deploy again
docker-compose up --renew-anon-volumes -d

## Open browser and check
# web1.domain
# web2.domain
# pma.domain/xxx ## user: root, pass: your secret MYSQL_ROOT_PASSWORD
```

### Auto-deploy
It works because of the deployed github-runner in server, 
which attached to the organization including such a repository.

Each time a commit pushed to master branch, the runner will be triggered
building and deploying the new changes to server

**Workflow**

Under "./.github/worflows/deploy.yml"
* Assign secrets and some github variables to Global env. variables
* Checkout new changes to "." (WORKING DIR of runner)
* Write 
    * MYSQL_INIT to ./mysql/init/init.sql
    * MYSQL_TEST to ./mysql/init/test.sh
    * PHP_PARAMS to ./nginx/conf.d/credentials.conf
    * SERVER_KEY to ./nginx/ssl/server.key
    * SERVER_PEM to ./nginx/ssl/server.pem
* SSH create tmp dir 
    * TMP_DIR: ~/tmp/[organization]/[repo name]
* Copy "." (all sources) to server, per scp, with secrets: DC_HOST, DC_KEY, DC_PORT, DC_USER
    * TARGET: ~/[organization]/[repo name]
* Backup all database from mysql container
    * TARGET: ~/backup/mysql
    * CMD: "docker exec mysql /usr/bin/mysqldump --all-databases -u"root" -p"$MYSQL_ROOT_PASSWORD" > $MYSQL_DUMPS_DIR/all_backups.sql 2>/dev/null || true"
* Generate configs
    * GENERATE_SCRIPT: TARGET/generate_configs.sh
    * ssl/sites/ssl.json -> ssl/wsites/[site].[pem|key]
    * conf.d/sites/auth.json -> conf.d/wsites/.[site]passwd
* Deploy new docker containers
    * Build: "docker-compose build --no-cache"                                                  
    * Remove: "docker-compose rm -f -s"
    * Create: "docker-compose up --renew-anon-volumes -d"
    * Remove TMP_DIR
* Allow permisson on target directory in server
    * TARGET: ~/[organization]/[repo name]
* Restore all backup database to the new mysql container
    * RESTORE_SCRIPT: TARGET/wait_for_restore.sh
    * SOURCE: ~/backup/mysql/all_backup.sql
    * CMD: "docker exec -i mysql /usr/bin/mysql -u"root" -p"$MYSQL_ROOT_PASSWORD" < $MYSQL_DUMPS_DIR/all_backups.sql 2>/dev/null || true"

    
