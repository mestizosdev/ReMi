# -*- coding: utf-8 -*-
from suds.client import Client
import ssl


class HttpClient(object):
    url = None
    status_receipt = None

    def __init__(self):
        self.url = 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'
        self.status_receipt = StatusReceipt()

    def download(self, access_key):
        """
        Download the XML SRI document, this method consume the SRI Web Service
        :param access_key: code of SRI document
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        client = Client(self.url)

        request_data = client.service.autorizacionComprobante(access_key)

        if request_data.numeroComprobantes == "0":
            self.status_receipt.status = 'La clave de acceso no está registrada'
            return False, self.status_receipt
        else:
            request_comprobante = request_data.autorizaciones.autorizacion
            if len(request_comprobante) > 0:

                self.status_receipt.authorization = request_comprobante[0].numeroAutorizacion
                self.status_receipt.authorization_date = str(request_comprobante[0].fechaAutorizacion)
                self.status_receipt.status = request_comprobante[0].estado
                self.status_receipt.receipt = str(request_comprobante[0].comprobante)

                print('Clave de Acceso: ' + request_data.claveAccesoConsultada)
                print('Autorización: ' + self.status_receipt.authorization)
                print('Fecha de Autorización: ' + self.status_receipt.authorization_date)
                print('Estado: ' + self.status_receipt.status)

                return True, self.status_receipt
            else:
                self.status_receipt.status = 'El comprobante no se encuentra autorizado'
                return False, self.status_receipt


class StatusReceipt(object):
    authorization = None
    authorization_date = None
    status = None
    receipt = None

    def __init__(self):
        self.authorization = ''
        self.authorization_date = ''
        self.status = ''
        self.receipt = ''
