CREATE SEQUENCE SEQ_TAXPAYERS INCREMENT BY 1 START WITH 1 MINVALUE 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER tr_seq_taxpayers
BEFORE INSERT ON remi_taxpayers
FOR EACH ROW
  WHEN (new.ID IS NULL)
BEGIN
  :new.ID := SEQ_TAXPAYERS.NEXTVAL;
END;
/


CREATE SEQUENCE SEQ_RECEIPTS INCREMENT BY 1 START WITH 1 MINVALUE 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER tr_seq_receipts
BEFORE INSERT ON remi_receipts
FOR EACH ROW
  WHEN (new.ID IS NULL)
BEGIN
  :new.ID := SEQ_RECEIPTS.NEXTVAL;
END;
/

CREATE SEQUENCE SEQ_INVOICES_DETAILS INCREMENT BY 1 START WITH 1 MINVALUE 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER tr_seq_invoides_details
BEFORE INSERT ON remi_invoices_details
FOR EACH ROW
  WHEN (new.ID IS NULL)
BEGIN
  :new.ID := SEQ_INVOICES_DETAILS.NEXTVAL;
END;
/