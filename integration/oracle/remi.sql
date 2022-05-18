CREATE SEQUENCE "SEQ_INVOICES_DETAILS" MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 41 NOCACHE ORDER NOCYCLE;

CREATE SEQUENCE "SEQ_RECEIPTS" MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 9 NOCACHE ORDER NOCYCLE;

CREATE SEQUENCE "SEQ_TAXES" MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 NOCACHE ORDER NOCYCLE;


CREATE TABLE "REMI_INVOICES_DETAILS" (
    "ID"                NUMBER(*, 0),
    "RECEIPT_ID"        NUMBER(*, 0),
    "LINE"              NUMBER(*, 0),
    "CODE"              VARCHAR2(280),
    "DESCRIPTION"       VARCHAR2(4000),
    "QUANTITY"          NUMBER(10, 6),
    "UNIT_PRICE"        NUMBER(10, 6),
    "DISCOUNT"          NUMBER(10, 6),
    "PRICE_WITHOUT_TAX" NUMBER(10, 6),
    PRIMARY KEY ("ID")
);

CREATE TABLE "REMI_RECEIPTS" (
    "ID"                      NUMBER(*, 0),
    "TAXPAYER_ID"             NUMBER(*, 0),
    "ACCESS_KEY"              VARCHAR2(280),
    "TYPE_RECEIPT"            VARCHAR2(280),
    "ESTABLISHMENT"           VARCHAR2(280),
    "EMISSION_POINT"          VARCHAR2(280),
    "SEQUENCE"                VARCHAR2(280),
    "DATE_EMISSION"           DATE,
    "AUTHORIZATION"           VARCHAR2(280),
    "DATE_AUTHORIZATION"      DATE,
    "RECEPTOR_IDENTIFICATION" VARCHAR2(280),
    "RECEPTOR_BUSINESS_NAME"  VARCHAR2(280),
    "TOTAL"                   NUMBER(10, 6),
    PRIMARY KEY ("ID")
);

CREATE TABLE "REMI_TAXES" (
    "ID"                NUMBER(*, 0),
    "INVOICE_DETAIL_ID" NUMBER(*, 0),
    "CODE"              VARCHAR2(280),
    "CODE_PERCENT"      VARCHAR2(280),
    "TARIFF"            NUMBER(10, 6),
    "BASE_VALUE"        NUMBER(10, 6),
    "VALUE"             NUMBER(10, 6),
    PRIMARY KEY ("ID")
);


CREATE OR REPLACE TRIGGER "TR_SEQ_INVOIDES_DETAILS" BEFORE
    INSERT ON remi_invoices_details
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := seq_invoices_details.nextval;
END;
/

CREATE OR REPLACE TRIGGER "TR_SEQ_RECEIPTS" BEFORE
    INSERT ON remi_receipts
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := seq_receipts.nextval;
END;
/

CREATE OR REPLACE TRIGGER "TR_SEQ_TAXES" BEFORE
    INSERT ON remi_taxes
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := seq_taxes.nextval;
END;
/


ALTER TABLE "REMI_INVOICES_DETAILS"
    ADD FOREIGN KEY ( "RECEIPT_ID" )
        REFERENCES "REMI_RECEIPTS" ( "ID" )
            ON DELETE CASCADE
    ENABLE;

ALTER TABLE "REMI_TAXES"
    ADD FOREIGN KEY ( "INVOICE_DETAIL_ID" )
        REFERENCES "REMI_INVOICES_DETAILS" ( "ID" )
            ON DELETE CASCADE
    ENABLE;