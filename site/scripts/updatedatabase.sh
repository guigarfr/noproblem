NOPROBLEM_DB='noproblemdb'
NOPROBLEM_DB_USER='pauly'
NOPROBLEM_DB_PASS='gaudenciaenguidanos'

NOPROBLEM_DB_USER_HOST="'$NOPROBLEM_DB_USER'@'localhost'"

mysql_login(){
	mysql --user $NOPROBLEM_DB_USER --password=$NOPROBLEM_DB_PASS
}

mysql_login_root(){
	mysql --user root -p
}


echo "Datos inicio sesion en mysql"
echo " - usuario  = $NOPROBLEM_DB_USER"
echo " - password = $NOPROBLEM_DB_PASS"
echo " - database = $NOPROBLEM_DB"
echo ""
echo "Voy a eliminar la base de datos antigua"
echo "drop database $NOPROBLEM_DB" | mysql_login
echo ""
echo "Voy a crear la base de datos nueva"
echo "create database $NOPROBLEM_DB" | mysql_login
echo ""
echo "Voy a permitir al usuario acceder a la db. Introduce tu clave de root mysql"
echo "grant usage on *.* to $NOPROBLEM_DB_USER_HOST identified by '$NOPROBLEM_DB_PASS'" | mysql_login_root
echo ""
echo "Voy a darle permisos al usuario. Introduce tu clave de root mysql"
echo "grant all privileges on $NOPROBLEM_DB.* to $NOPROBLEM_DB_USER_HOST" | mysql_login_root
echo ""
echo "Terminado! Ejecuta python manage.py syncdb en tu sitio django"
exit