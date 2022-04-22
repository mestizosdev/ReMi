mysql -h 172.17.0.3 -P 3306 --user=remi --password=r remi

/usr/lib64/libmyodbc5.so

[ODBC Data Sources]
test_mysql = MySQL ODBC Driver 5.1

[test_mysql]
Driver      = /usr/lib64/libmyodbc3.so
DATABASE    = oracletest
DESCRIPTION = Conexion a MySQL ODBC
PORT        = 3306
SERVER      = SERVIDOR_MYSQL# UID       = oracleconn
# PWD       = demo
CHARSET     = latin1
TRACEFILE   = /tmp/myodbc-demodsn.trc
TRACE       = ON

