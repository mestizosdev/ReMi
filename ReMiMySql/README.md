# ReMi
Recover SRI XML receipts

## Software
* Python 3.6 or above
* MySql 5 or Mariadb 5 or above

## MySql
```
mysql -h localhost -P 3306 --user=root --password=Mi_Secreto0
mycli -h 172.17.0.1 -u remi -p Mi_Secreto0
```
List databases
```
show databases;
```
List users
```
SELECT User, Host, Password FROM mysql.user;
```
```
CREATE SCHEMA `remi`;

CREATE USER 'remi'@'%' IDENTIFIED BY 'Mi_Secreto0';

GRANT ALL PRIVILEGES ON remi.* TO 'remi'@'%' WITH GRANT OPTION;

ALTER USER 'remi'@'%' IDENTIFIED BY 'Mi_Secreto0';
```
update password for Mariadb
```
set password for 'remi'@'%' = password('Mi_Secreto0');
```
```
FLUSH PRIVILEGES;
```
### Create virualenv (bash, zsh, ...)
```
virtualenv venv
```
```
. ./venv/bin/activate
```
### Migrate database
```
flask db init
```
```
flask db migrate
```
```
flask db upgrade
```
### Configuration (bash, zsh, ...)
```
export FLASK_APP=app
```
```
export FLASK_ENV=development
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
## Docker compose
```
docker-compose down
```
```
docker-compose up -d
```
## Firewall ufw 
```
ufw allow in on docker0 to any port 3306
```
## Run in production mode
```
gunicorn --bind=0.0.0.0:5000 app:app
```