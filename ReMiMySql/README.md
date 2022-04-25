# ReMi
Recover SRI XML receipts

## Software
* Python 3.6 or above
* MySql 5 or above

## uWSGI
```
uwsgi --ini ./remi.ini
```

## MySql
```
CREATE SCHEMA `remi` DEFAULT CHARACTER SET utf8 ;

CREATE USER 'remi'@'%' IDENTIFIED BY 'No_piratear1';

GRANT ALL PRIVILEGES ON remi.* TO 'remi'@'%' WITH GRANT OPTION;

ALTER USER 'remi'@'%' IDENTIFIED BY 'No_piratear1';

FLUSH PRIVILEGES;
```
## Docker
```
docker build -t remi .
docker run -it --publish 5000:5000 remi
docker logs pedantic_colden
```
with system variables
```
docker run -it -e 'DB_HOST=172.17.0.1' -p 5000:5000 remi
```
## Firewall ufw 
```
ufw allow in on docker0 to any port 3306
```
## Run in production mode
```
gunicorn --bind=0.0.0.0:5000 app:app
```