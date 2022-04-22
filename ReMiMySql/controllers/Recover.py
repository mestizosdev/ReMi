# -*- coding: utf-8 -*-
from flask_restful import Resource
from utils.AccessKey import AccessKey
from utils.HttpClient import HttpClient
from utils.AuthorizedFile import AuthorizedFile
from recovers.Invoice import Invoice


class Recover(Resource):
    @classmethod
    def get(cls, access_key):
        try:
            if not AccessKey.is_valid(access_key):
                return {'message': 'Clave de acceso no valida'}, 422

            client = HttpClient()
            is_success, status_receipt = client.download(access_key)

            if not is_success:
                return {'message': status_receipt.status}, 404

            authorized_file = AuthorizedFile()
            type_receipt, file_xml = authorized_file.save(status_receipt.receipt, access_key)

            receipt_id = None
            if type_receipt == 'FACTURA':
                invoice = Invoice(status_receipt)
                receipt_id = invoice.deserialize(file_xml)

            return {'receipt': receipt_id}

        except Exception as e:
            return str(e), 501
