#!/bin/bash

echo "Restoring..."

mysql_running=$( docker inspect -f '{{.State.Running}}' mysql )
count=180
# continue until $n equals 5
while [ -z "$mysql_running" -a $count -ge 0 ]
do
	echo "MySql started $mysql_running. ($count)"
	sleep 1 # sleep 1 s
	count=$((count - 1))
done

echo "From path $2 ..."
$( docker exec -i mysql /usr/bin/mysql -u"root" -p"$1" < "$2" )

echo "Restored!!!"
