DECLARE
  --l_principal VARCHAR2(20) := 'APEX_040200';
  --l_principal VARCHAR2(20) := 'APEX_050000';
  --l_principal VARCHAR2(20) := 'APEX_050100';
  --l_principal VARCHAR2(20) := 'APEX_180200';
  --l_principal VARCHAR2(20) := 'APEX_190100';
  l_principal VARCHAR2(20) := 'APEX_200200';
BEGIN
  DBMS_NETWORK_ACL_ADMIN.create_acl (
    acl          => 'server_remi_acl.xml', 
    description  => 'An ACL for the Server ReMi',
    principal    => l_principal,
    is_grant     => TRUE, 
    privilege    => 'connect',
    start_date   => SYSTIMESTAMP,
    end_date     => NULL);

  DBMS_NETWORK_ACL_ADMIN.assign_acl (
    acl         => 'server_remi_acl.xml',
    host        => '192.168.0.120', 
    lower_port  => 5000,
    upper_port  => 5000); 

  COMMIT;
END;
/