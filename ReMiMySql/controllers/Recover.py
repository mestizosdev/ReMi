# -*- coding: utf-8 -*-
from flask_restful import Resource
import logging
logger = logging.getLogger(__name__)
from utils.AccessKey import AccessKey
from utils.HttpClient import HttpClient
from utils.AuthorizedFile import AuthorizedFile
from recovers.Invoice import Invoice
from models.Receipt import Receipt
from models.TaxPayer import TaxPayer


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

            receipt = Receipt.query.filter_by(id=receipt_id).first()
            tax_payer = TaxPayer.query.filter_by(id=receipt.taxpayer_id).first()

            return {'type_receipt': type_receipt,
                    'receipt': receipt.serialize(),
                    'supplier': tax_payer.serialize()}

        except Exception as e:
            logger.error('Recover ' + access_key + ' ' + str(e))
            return {'message': str(e)}, 501
