# -*- coding: utf-8 -*-
import datetime

from app import db
from sqlalchemy import insert

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

        taxpayer_id = 0
        if taxpayer.count() == 0:
            statement = (
                insert(TaxPayer).values(
                    identification=identification,
                    business_name=business_name,
                    address=address
                )
            )

            result = db.session.execute(statement)
            db.session.commit()

            for row in result.inserted_primary_key:
                taxpayer_id = row
        else:
            taxpayer_id = taxpayer.first().id

        date_emission = ''
        receptor_identification = ''
        receptor_business_name = ''

        for child in object_receipt.find('infoFactura'):
            if child.tag == 'fechaEmision':
                date_emission = datetime.datetime.strptime(child.text, '%d/%m/%Y').date()
            if child.tag == 'identificacionComprador':
                receptor_identification = child.text
            if child.tag == 'razonSocialComprador':
                receptor_business_name = child.text
            print(child.tag, child.text)

        receipt = Receipt.query.filter_by(access_key=self.status_receipt.access_key)

        if receipt.count() > 0:
            db.session.delete(receipt.first())
            db.session.commit()

        new_receipt = Receipt(taxpayer_id=taxpayer_id,
                              access_key=self.status_receipt.access_key,
                              type_receipt='FACTURA',
                              establishment=establishment,
                              emission_point=emission_point,
                              sequence=sequence,
                              date_emission=date_emission,
                              authorization=self.status_receipt.authorization,
                              date_authorization=datetime.datetime.strptime(self.status_receipt.authorization_date[0:19], '%Y-%m-%d %H:%M:%S'),
                              receptor_identification=receptor_identification,
                              receptor_business_name=receptor_business_name)

        db.session.add(new_receipt)
        db.session.commit()

        detalles = object_receipt.iter("detalle")

        for detalle in detalles:
            detalle_children = detalle.getchildren()

            for elementos in detalle_children:
                print(elementos.tag, elementos.text)
