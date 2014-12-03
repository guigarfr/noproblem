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
echo "Voy a eliminar la base de datos antigua_root. Introduce clave de root mysql:"
echo "drop database $NOPROBLEM_DB" | mysql_login_root
echo ""
echo "Voy a crear la nueva db. Introduce clave de root mysql"
./dbcreate.sh $NOPROBLEM_DB $NOPROBLEM_DB_USER $NOPROBLEM_DB_PASS
echo ""
echo "Terminado! Ejecuta python manage.py syncdb en tu sitio django"
exit
