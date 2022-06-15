SELECT username,
       account_status,
       TO_CHAR(lock_date, 'DD-MON-YYYY') AS lock_date,
       TO_CHAR(expiry_date, 'DD-MON-YYYY') AS expiry_date,
       default_tablespace,
       temporary_tablespace
FROM   dba_users
WHERE  username LIKE UPPER('%APEX%')
ORDER BY username;

SELECT * FROM DBA_NETWORK_ACLS;
SELECT * FROM DBA_NETWORK_ACL_PRIVILEGES;

exec DBMS_NETWORK_ACL_ADMIN.DROP_ACL (acl => '/sys/acls/server_remi_acl.xml' );

SELECT PRINCIPAL, HOST, lower_port, upper_port, acl, 'connect' AS PRIVILEGE, 
    DECODE(DBMS_NETWORK_ACL_ADMIN.CHECK_PRIVILEGE_ACLID(aclid, PRINCIPAL, 'connect'), 1,'GRANTED', 0,'DENIED', NULL) PRIVILEGE_STATUS
FROM DBA_NETWORK_ACLS
    JOIN DBA_NETWORK_ACL_PRIVILEGES USING (ACL, ACLID)  
UNION ALL
SELECT PRINCIPAL, HOST, NULL lower_port, NULL upper_port, acl, 'resolve' AS PRIVILEGE, 
    DECODE(DBMS_NETWORK_ACL_ADMIN.CHECK_PRIVILEGE_ACLID(aclid, PRINCIPAL, 'resolve'), 1,'GRANTED', 0,'DENIED', NULL) PRIVILEGE_STATUS
FROM DBA_NETWORK_ACLS
    JOIN DBA_NETWORK_ACL_PRIVILEGES USING (ACL, ACLID);