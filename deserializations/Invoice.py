# -*- coding: utf-8 -*-
import datetime

from app import db
from sqlalchemy import text

from models.Receipt import Receipt
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
        establishment = ''
        emission_point = ''
        sequence = ''

        for child in object_receipt.find('infoTributaria'):
            if child.tag == 'ruc':
                identification = child.text
            if child.tag == 'razonSocial':
                business_name = child.text
            if child.tag == 'dirMatriz':
                address = child.text
            if child.tag == 'estab':
                establishment = child.text
            if child.tag == 'ptoEmi':
                emission_point = child.text
            if child.tag == 'secuencial':
                sequence = child.text

        taxpayer = TaxPayer.query.filter_by(identification=identification)

        taxpayer_id = taxpayer.first().id

        if taxpayer.count() == 0:
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
                result = db.session.execute(statement, line)
            db.session.commit()

        date_emission = ''
        receptor_identification = ''
        receptor_business_name = ''

        for child in object_receipt.find('infoFactura'):
            if child.tag == 'fechaEmision':
                date_emission = child.text
            if child.tag == 'identificacionComprador':
                receptor_identification = child.text
            if child.tag == 'razonSocialComprador':
                receptor_business_name = child.text
            print(child.tag, child.text)

        receipt = Receipt(taxpayer_id=taxpayer_id,
                          access_key=self.status_receipt.access_key,
                          type_receipt='FACTURA',
                          establishment=establishment,
                          emission_point=emission_point,
                          sequence=sequence,
                          date_emission=datetime.datetime.now(),
                          authorization=self.status_receipt.authorization,
                          date_authorization=datetime.datetime.now(),
                          receptor_identification=receptor_identification,
                          receptor_business_name=receptor_business_name)

        print(vars(receipt))

        db.session.add(receipt)
        db.session.commit()

        detalles = object_receipt.iter("detalle")

        for detalle in detalles:
            detalle_children = detalle.getchildren()

            for elementos in detalle_children:
                print(elementos.tag, elementos.text)
