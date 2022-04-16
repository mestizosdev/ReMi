# ReMi
Recover SRI XML receipts

## Software
* Python 3.8 or above
* Postgres 13 or above
* Oracle 11g R2 or above
### Create database and user in Windows
```
psql
```
```
create database customer;
```
```
create user developer with encrypted password 'd';
```
```
grant all privileges on database customer to developer;
```
```
psql -d customer -U developer -W
```
### Create database on GNU/Linux and MacOS with Postgres.app
```
createdb customer
```
```
createuser developer
```
```
psql
```
or
```
psql -d database -U user -W
```
```
grant all privileges on database customer to developer;
```
```
alter user developer with encrypted password 'd';
```
### Create virualenv (bash, zsh, ...)
```
virtualenv venv
```
```
. ./venv/bin/activate
```
### Create virualenv (cmd, powershell)
```
virtualenv venv
```
```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
```
.\venv\Scripts\activate
```
### Install dependencies
```
pip install -r requirements.txt
```
### Configuration (bash, zsh, ...)
```
export FLASK_APP=app
```
```
export FLASK_ENV=development
```
### Configuration (cmd)
```
set FLASK_APP=app
```
```
set FLASK_ENV=development
```
### Configuration (Powershell)
```
$env:FLASK_APP = "app"
```
```
$env:FLASK_ENV = "development"
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
### Create view
```
flask views create
```
### Seeder
```
flask seed
```
### Migrate data from .csv files
```
flask migrate
```
### Run
```
flask run
```
#### Custom port
```
flask run --port=5001
```
### Test
```
pytest
```
or
```
pytest -s
```
### Drop view
```
flask views drop
```
### Drop tables
```
flask db downgrade
```
### Drop all tables from databse
```
select 'drop table if exists "' || tablename || '" cascade;' 
from pg_tables
where schemaname = 'public';
```
