CREATE OR REPLACE PACKAGE PKG_REMI AS 

  function fun_version return varchar2; 
  function fun_index return varchar2; 
  function fun_recover(p_access_key varchar2) return number;
  
END PKG_REMI;
/


CREATE OR REPLACE PACKAGE BODY PKG_REMI AS

  function fun_version return varchar2 AS
    l_clob   CLOB;
  BEGIN
    l_clob := apex_web_service.make_rest_request(
        p_url => 'http://192.168.0.120:5000/version', 
        p_http_method => 'GET');
    
    dbms_output.put_line('status=' || apex_web_service.g_status_code);
    dbms_output.put_line('l_clob=' || l_clob);
    APEX_JSON.parse(l_clob);
    
    RETURN APEX_JSON.get_varchar2(p_path => 'version');
  END fun_version;

  function fun_index return varchar2 AS
    l_clob   CLOB;
  BEGIN
    l_clob := apex_web_service.make_rest_request(
        p_url => 'http://192.168.0.120:5000', 
        p_http_method => 'GET');
    
    dbms_output.put_line('l_clob=' || l_clob);
    APEX_JSON.parse(l_clob);
    
    DBMS_OUTPUT.put_line(
        APEX_JSON.get_varchar2(p_path => 'application.name')
    );
    
    RETURN APEX_JSON.get_varchar2(p_path => 'application.name');
  END fun_index;

  function fun_recover(p_access_key varchar2) return number AS
  BEGIN
    -- TODO: Implementation required for function PKG_REMI.fun_recover
    RETURN NULL;
  END fun_recover;

END PKG_REMI;
/
