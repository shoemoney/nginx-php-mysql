#!/bin/bash
#$1 host ip mysql
#$2 port mysql
#$3 user file
#$4 passwd mysql
#$5 backup file

echo "mysql binding ..."

until mysql -h $1 -P $2 -u"$3" -p"$4" --protocol=tcp -e "SHOW DATABASES;"; do
  >&2 echo "mysql UNAVAILABLE - sleeping 10s"
  sleep 10
done

>&2 echo "mysql UP - restoring"
exec docker exec -i mysql mysql -h $1 -P $2 --protocol=tcp -u"$3" -p"$4" < "$5"

echo "mysql restored !!!"
