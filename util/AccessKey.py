# -*- coding: utf-8 -*-

class AccessKey(object):

    def verify_document_type(access_key):
        """
        Verifica si la clave de acceso es de una Factura, Retención, Nota de Crédito, Nota de Débito o Guía de Remisión
        :param clave:
        :return:
        """
        if (access_key[8:8 + 2]) == "01":
            return "FACTURA"
        elif (access_key[8:8 + 2]) == "04":
            return "NOTA DE CRÉDITO"
        elif (access_key[8:8 + 2]) == "05":
            return "NOTA DE DÉBITO"
        elif (access_key[8:8 + 2]) == "06":
            return "GUÍA DE REMISIÓN"
        elif (access_key[8:8 + 2]) == "07":
            return "COMPROBANTE DE RETENCIÓN"

        return "NO DEFINIDO"

    def is_valid(access_key):
        """
        Verify access key
        :param access_key:
        """
        if len(access_key) == 49:
            return True
        else:
            return False
