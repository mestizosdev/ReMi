# -*- coding: utf-8 -*-

class AccessKey(object):

    def document_type(access_key):
        """
        Is: Factura, Liquidación, Retención, Nota de Crédito, Nota de Débito or Guía de Remisión
        :param access_key
        :return: string
        """
        if (access_key[8:8 + 2]) == '01':
            return 'FACTURA'
        if (access_key[8:8 + 2]) == '03':
            return 'LIQUIDACION'
        elif (access_key[8:8 + 2]) == '04':
            return 'NOTA_CREDITO'
        elif (access_key[8:8 + 2]) == '05':
            return 'NOTA_DEBITO'
        elif (access_key[8:8 + 2]) == '06':
            return 'GUIA'
        elif (access_key[8:8 + 2]) == '07':
            return 'RETENCION'

        return 'not defined'

    def is_valid(access_key):
        """
        Verify access key
        :param access_key:
        """
        if len(access_key) == 49:
            return True
        else:
            return False

    def get_identification(access_key):
        """
        Extract identification
        :param access_key:
        :return identification:
        """
        return access_key[10:10 + 13]

    def get_year(access_key):
        """
        Extract year
        :param access_key:
        :return identification:
        """
        return access_key[4:4 + 4]

    def get_month(access_key):
        """
        Extract month
        :param access_key:
        :return identification:
        """
        return access_key[2:2 + 2]
