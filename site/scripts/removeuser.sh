#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65
MYSQL=`which mysql`

echo "$1, $2"

 
Q1="SHOW GRANTS FOR '$2'@'localhost';"
Q2="REVOKE ALL PRIVILEGES, GRANT OPTION FROM '$2'@'localhost';"
Q3="FLUSH PRIVILEGES;"
Q4="DROP USER '$2'@'localhost';"
SQL="${Q1}${Q2}${Q3}${Q4}"
 
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 dbname dbuser"
  exit $E_BADARGS
fi
echo "Mysql: $MYSQL"
echo "Command: $SQL" 
$MYSQL -uroot -p -e "$SQL"

