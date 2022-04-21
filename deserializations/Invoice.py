# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import text
from sqlalchemy.sql import func

from models.TaxPayer import TaxPayer
from deserializations.StatusReceipt import StatusReceipt
from utils.AuthorizedFile import AuthorizedFile


class Invoice(object):
    status_receipt = StatusReceipt()

    def __init__(self, status_receipt):
        self.status_receipt = status_receipt

    def deserialize(self, file_xml):
        authorized_file = AuthorizedFile()
        object_receipt = authorized_file.xml_to_object(file_xml)

        print(object_receipt.tag)
        identification = ''
        business_name = ''
        address = ''

        for child in object_receipt.find('infoTributaria'):
            if child.tag == 'ruc':
                identification = child.text
            if child.tag == 'razonSocial':
                business_name = child.text
            if child.tag == 'dirMatriz':
                address = child.text

        count_taxpayer = TaxPayer.query.filter_by(identification=identification).count()

        if count_taxpayer == 0:
            data = (
                {'identification': identification,
                 'business_name': business_name,
                 'address': address},)

            statement = text('''INSERT INTO remi_taxpayers (
                                    identification,
                                    business_name,
                                    address,
                                    status
                                ) VALUES (
                                    :identification,
                                    :business_name,
                                    :address,
                                    'Activo'
                                )''')

            for line in data:
                db.session.execute(statement, line)
            db.session.commit()

        for child in object_receipt.find('infoFactura'):
            print(child.tag, child.text)

        detalles = object_receipt.iter("detalle")

        for detalle in detalles:
            detalle_children = detalle.getchildren()

            for elementos in detalle_children:
                print(elementos.tag, elementos.text)
