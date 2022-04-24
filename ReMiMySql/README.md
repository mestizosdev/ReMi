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

CREATE USER 'remi'@'%' IDENTIFIED BY 'remiremi';

GRANT ALL PRIVILEGES ON remi.* TO 'remi'@'%' WITH GRANT OPTION;

ALTER USER 'remi'@'%' IDENTIFIED BY 'remiremi';

FLUSH PRIVILEGES;
```
