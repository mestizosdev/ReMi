CREATE OR REPLACE PACKAGE pkg_remi AS
    default_server CONSTANT VARCHAR2(100) := 'http://192.168.0.120:5000';
    FUNCTION fun_version RETURN VARCHAR2;

    FUNCTION fun_index RETURN VARCHAR2;

    FUNCTION fun_recover (
        p_access_key VARCHAR2
    ) RETURN VARCHAR2;

    FUNCTION fun_supplier (
        p_clob CLOB
    ) RETURN NUMBER;
    
    FUNCTION fun_receipt (
        p_clob CLOB,
        p_supplier_id number
    ) RETURN NUMBER;
    
    procedure pro_invoice_detail (
        p_clob CLOB,
        p_receipt_id number
    );

    FUNCTION fun_save_supplier (
        p_identification VARCHAR2,
        p_business_name  VARCHAR2,
        p_trade_name     VARCHAR2,
        p_address        VARCHAR2
    ) RETURN NUMBER;

END pkg_remi;
/


CREATE OR REPLACE PACKAGE BODY pkg_remi AS

    FUNCTION fun_version RETURN VARCHAR2 AS
        l_clob CLOB;
    BEGIN
        l_clob := apex_web_service.make_rest_request(p_url => default_server || '/version', p_http_method => 'GET');

        dbms_output.put_line('status=' || apex_web_service.g_status_code);
        dbms_output.put_line('l_clob=' || l_clob);
        apex_json.parse(l_clob);
        RETURN apex_json.get_varchar2(p_path => 'version');
    END fun_version;

    FUNCTION fun_index RETURN VARCHAR2 AS
        l_clob CLOB;
    BEGIN
        l_clob := apex_web_service.make_rest_request(p_url => default_server, p_http_method => 'GET');
        dbms_output.put_line('l_clob=' || l_clob);
        apex_json.parse(l_clob);
        dbms_output.put_line(apex_json.get_varchar2(p_path => 'application.name'));
        RETURN apex_json.get_varchar2(p_path => 'application.name');
    END fun_index;

    FUNCTION fun_recover (
        p_access_key VARCHAR2
    ) RETURN VARCHAR2 AS
        v_clob     CLOB;
        v_status   NUMBER;
        l_members  wwv_flow_t_varchar2;
        v_supplier NUMBER;
        v_receipt  NUMBER;
    BEGIN
        v_clob := apex_web_service.make_rest_request(p_url => default_server
                                                              || '/recover/'
                                                              || p_access_key, p_http_method => 'GET');

        v_status := apex_web_service.g_status_code;
        IF v_status = 200 THEN
            dbms_output.put_line('v_clob=' || v_clob);
            v_supplier := fun_supplier(v_clob);
            dbms_output.put_line('Supplier id ' || v_supplier);
            v_receipt := fun_receipt(v_clob, v_supplier);
            dbms_output.put_line('Receipt id ' || v_receipt);
            pro_invoice_detail(v_clob, v_receipt);
        ELSE
            apex_json.parse(v_clob);
            RETURN apex_json.get_varchar2(p_path => 'message');
        END IF;

        COMMIT;
        RETURN 'Success';
    EXCEPTION
        WHEN UTL_HTTP.transfer_timeout THEN
            RETURN 'HTTP timeout';
         WHEN others THEN
            RETURN 'Call apex_web_service error';
    END fun_recover;

    FUNCTION fun_supplier (
        p_clob CLOB
    ) RETURN NUMBER AS

        v_members        wwv_flow_t_varchar2;
        v_identification VARCHAR2(20);
        v_business_name  VARCHAR2(500);
        v_trade_name     VARCHAR2(500);
        v_address        VARCHAR2(500);
        v_supplier_id    NUMBER;
    BEGIN
        apex_json.parse(p_clob);
        v_members := apex_json.get_members(p_path => 'supplier');
        FOR i IN 1..v_members.count LOOP
            dbms_output.put_line(v_members(i)
                                 || ' '
                                 || apex_json.get_varchar2(p_path => 'supplier.' || v_members(i)));

            IF v_members(i) = 'identification' THEN 
                v_identification := apex_json.get_varchar2(p_path => 'supplier.' || v_members(i));

            ELSIF v_members(i) = 'business_name' THEN
                v_business_name := apex_json.get_varchar2(p_path => 'supplier.' || v_members(i));
            ELSIF v_members(i) = 'trade_name' THEN
                v_trade_name := apex_json.get_varchar2(p_path => 'supplier.' || v_members(i));
            ELSIF v_members(i) = 'address' THEN
                v_address := apex_json.get_varchar2(p_path => 'supplier.' || v_members(i));
            END IF;

        END LOOP;

        BEGIN
            SELECT
                cod_proveedor
            INTO v_supplier_id
            FROM
                v_proveedor
            WHERE
                    documento = v_identification
                AND ROWNUM = 1;

        EXCEPTION
            WHEN no_data_found THEN
                v_supplier_id := fun_save_supplier(v_identification, v_business_name, v_trade_name, v_address);
            WHEN OTHERS THEN
                RETURN -1;
        END;

        RETURN v_supplier_id;
    END fun_supplier;

    FUNCTION fun_save_supplier (
        p_identification VARCHAR2,
        p_business_name  VARCHAR2,
        p_trade_name     VARCHAR2,
        p_address        VARCHAR2
    ) RETURN NUMBER AS
        v_people_id   NUMBER;
        v_supplier_id NUMBER;
    BEGIN
        v_people_id := s_gnr_persona.nextval;
        SELECT
            nvl(MAX(cod_proveedor), 0) + 1
        INTO v_supplier_id
        FROM
            inv_proveedor
        WHERE
            cod_empresa = '01';

        INSERT INTO gnr_persona (
            cod_empresa,
            cod_persona,
            tipo_persona,
            documento,
            cod_documento,
            razon_social,
            nombre_comercial,
            direccion
        ) VALUES (
            '01',
            v_people_id,
            fun_is_natural_juridico(p_identification),
            p_identification,
            1,
            p_business_name,
            p_trade_name,
            p_address
        );

        INSERT INTO inv_proveedor (
            cod_empresa,
            cod_proveedor,
            cod_persona,
            beneficiario,
            cod_grupo,
            estado,
            fecha_creacion,
            fecha_estado
        ) VALUES (
            '01',
            v_supplier_id,
            v_people_id,
            '.',
            '01',
            'A',
            sysdate,
            sysdate
        );

        RETURN v_supplier_id;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('fun_save_supplier '
                                 || sqlerrm
                                 || ' '
                                 || sqlcode);
            RETURN -1;
    END fun_save_supplier;

    FUNCTION fun_receipt (
        p_clob        CLOB,
        p_supplier_id NUMBER
    ) RETURN NUMBER AS

        v_members                 wwv_flow_t_varchar2;
        v_type_receipt            VARCHAR2(50);
        v_access_key              VARCHAR2(100);
        v_establishment           VARCHAR2(10);
        v_emission_point          VARCHAR2(10);
        v_sequence                VARCHAR2(50);
        v_date_emission           DATE;
        v_authorization           VARCHAR2(100);
        v_date_authorization      DATE;
        v_receptor_identification VARCHAR2(50);
        v_receptor_business_name  VARCHAR2(500);
        v_receipt_id              NUMBER;
    BEGIN
        apex_json.parse(p_clob);
        v_members := apex_json.get_members(p_path => 'receipt');
        FOR i IN 1..v_members.count LOOP
            IF v_members(i) = 'type_receipt' THEN
                v_type_receipt := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));

            ELSIF v_members(i) = 'access_key' THEN
                v_access_key := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'establishment' THEN
                v_establishment := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'emission_point' THEN
                v_emission_point := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'sequence' THEN
                v_sequence := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'date_emission' THEN
                v_date_emission := apex_json.get_date(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'authorization' THEN
                v_authorization := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'date_authorization' THEN
                v_date_authorization := apex_json.get_date(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'receptor_identification' THEN
                v_receptor_identification := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            ELSIF v_members(i) = 'receptor_business_name' THEN
                v_receptor_business_name := apex_json.get_varchar2(p_path => 'receipt.' || v_members(i));
            END IF;
        END LOOP;

        DELETE remi_receipts
        WHERE
            access_key = v_access_key;

        INSERT INTO remi_receipts (
            taxpayer_id,
            access_key,
            type_receipt,
            establishment,
            emission_point,
            sequence,
            date_emission,
            authorization,
            date_authorization,
            receptor_identification,
            receptor_business_name,
            total
        ) VALUES (
            p_supplier_id,
            v_access_key,
            v_type_receipt,
            v_establishment,
            v_emission_point,
            v_sequence,
            v_date_emission,
            v_authorization,
            v_date_authorization,
            v_receptor_identification,
            v_receptor_business_name,
            0
        ) RETURNING id INTO v_receipt_id;

        RETURN v_receipt_id;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('fun_receipt '
                                 || sqlerrm
                                 || ' '
                                 || sqlcode);
            RETURN -1;
    END fun_receipt;

    PROCEDURE pro_invoice_detail (
        p_clob       CLOB,
        p_receipt_id NUMBER
    ) AS
        v_paths     apex_t_varchar2;
        v_paths_tax apex_t_varchar2;
        v_detail_id NUMBER;
    BEGIN
        apex_json.parse(p_clob);
        v_paths := apex_json.find_paths_like(p_return_path => 'receipt.details[%]');
        dbms_output.put_line('Matching Paths: ' || v_paths.count);
        FOR i IN 1..v_paths.count LOOP
            dbms_output.put_line('Detail: '
                                 || apex_json.get_varchar2(p_path => v_paths(i)
                                                                     || '.code')
                                 || ' '
                                 || apex_json.get_varchar2(p_path => v_paths(i)
                                                                     || '.description'));

            v_paths_tax := apex_json.find_paths_like(p_return_path => v_paths(i)
                                                                      || '.taxes[%]');

            dbms_output.put_line('Matching Paths Tax: ' || v_paths_tax.count);
            INSERT INTO remi_invoices_details (
                receipt_id,
                line,
                code,
                description,
                quantity,
                unit_price,
                discount,
                price_without_tax
            ) VALUES (
                p_receipt_id,
                apex_json.get_number(p_path => v_paths(i)
                                               || '.line'),
                apex_json.get_varchar2(p_path => v_paths(i)
                                                 || '.code'),
                apex_json.get_varchar2(p_path => v_paths(i)
                                                 || '.description'),
                apex_json.get_number(p_path => v_paths(i)
                                               || '.quantity'),
                apex_json.get_number(p_path => v_paths(i)
                                               || '.unit_price'),
                apex_json.get_number(p_path => v_paths(i)
                                               || '.discount'),
                apex_json.get_number(p_path => v_paths(i)
                                               || '.price_without_tax')
            ) RETURNING id INTO v_detail_id;

            FOR i IN 1..v_paths_tax.count LOOP
                INSERT INTO remi_taxes (
                    invoice_detail_id,
                    code,
                    code_percent,
                    tariff,
                    base_value,
                    value
                ) VALUES (
                    v_detail_id,
                    apex_json.get_varchar2(p_path => v_paths_tax(i)
                                                     || '.code'),
                    apex_json.get_varchar2(p_path => v_paths_tax(i)
                                                     || '.code_percent'),
                    apex_json.get_number(p_path => v_paths_tax(i)
                                                   || '.tariff'),
                    apex_json.get_number(p_path => v_paths_tax(i)
                                                   || '.base_value'),
                    apex_json.get_number(p_path => v_paths_tax(i)
                                                   || '.value')
                );

            END LOOP;

        END LOOP;

    END pro_invoice_detail;

END pkg_remi;
/
