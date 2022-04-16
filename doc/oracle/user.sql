create user remi identified by r;
-- USER SQL
ALTER USER "REMI"
DEFAULT TABLESPACE "USERS"
TEMPORARY TABLESPACE "TEMP"
ACCOUNT UNLOCK ;

-- QUOTAS
ALTER USER "REMI" QUOTA UNLIMITED ON "USERS";

-- ROLES
GRANT "RESOURCE" TO "REMI" ;
GRANT "CONNECT" TO "REMI" ;

-- SYSTEM PRIVILEGES
GRANT CREATE ANY SEQUENCE TO "REMI" ;
GRANT CREATE ANY TRIGGER TO "REMI" ;

-- DROP USER
--drop user remi cascade;