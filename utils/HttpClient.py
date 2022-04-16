# -*- coding: utf-8 -*-
from suds.client import Client
import ssl


class HttpClient(object):
    url = None

    def __init__(self):
        self.url = 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'

    def download(self, access_key):
        """
        Download the XML SRI document, this method consume the SRI Web Service
        :param access_key: code of SRI document
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        client = Client(self.url)

        request_data = client.service.autorizacionComprobante(access_key)

        if request_data.numeroComprobantes == "0":
            return False, 'La clave de acceso no está registrada'
        else:
            request_comprobante = request_data.autorizaciones.autorizacion
            if len(request_comprobante) > 0:
                print('Clave de Acceso: ' + request_data.claveAccesoConsultada)
                print('Estado: ' + request_comprobante[0].estado)

                return True, str(request_comprobante[0].comprobante)
            else:
                return False, 'El comprobante no se encuentra autorizado'


