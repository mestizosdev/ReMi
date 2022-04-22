# -*- coding: utf-8 -*-
import datetime

from app import db

from models.InvoiceDetail import InvoiceDetail
from models.Receipt import Receipt
from models.Tax import Tax
from models.TaxPayer import TaxPayer
from recovers.StatusReceipt import StatusReceipt
from utils.AuthorizedFile import AuthorizedFile


class Invoice(object):
    status_receipt = StatusReceipt()

    def __init__(self, status_receipt):
        self.status_receipt = status_receipt

    def deserialize(self, file_xml):
        authorized_file = AuthorizedFile()
        object_receipt = authorized_file.xml_to_object(file_xml)

        incoming_taxpayer = TaxPayer()
        establishment = ''
        emission_point = ''
        sequence = ''

        for child in object_receipt.find('infoTributaria'):
            if child.tag == 'ruc':
                incoming_taxpayer.identification = child.text
            if child.tag == 'razonSocial':
                incoming_taxpayer.business_name = child.text
            if child.tag == 'nombreComercial':
                incoming_taxpayer.trade_name = child.text
            if child.tag == 'dirMatriz':
                incoming_taxpayer.address = child.text
            if child.tag == 'estab':
                establishment = child.text
            if child.tag == 'ptoEmi':
                emission_point = child.text
            if child.tag == 'secuencial':
                sequence = child.text

        taxpayer = TaxPayer.query.filter_by(identification=incoming_taxpayer.identification)

        taxpayer_id = None
        if taxpayer.count() == 0:
            db.session.add(incoming_taxpayer)
            db.session.commit()

            taxpayer_id = incoming_taxpayer.id
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

        # Delete receipt if exist
        if receipt.count() > 0:
            db.session.delete(receipt.first())
            db.session.commit()

        # Create new or again receipt
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

        detalles = object_receipt.iter("detalle")

        line = 1
        for detalle in detalles:
            detalle_children = detalle.getchildren()
            invoice_detail = None

            code = None
            description = None
            quantity = 0.0
            unit_price = 0.0,
            discount = 0.0,
            price_without_tax = 0.0

            for elementos in detalle_children:
                if elementos.tag == 'codigoPrincipal':
                    code = elementos.text
                if elementos.tag == 'descripcion':
                    description = elementos.text
                if elementos.tag == 'cantidad':
                    quantity = float(elementos.text)
                if elementos.tag == 'precioUnitario':
                    unit_price = float(elementos.text)
                if elementos.tag == 'descuento':
                    discount = float(elementos.text)
                if elementos.tag == 'precioTotalSinImpuesto':
                    price_without_tax = float(elementos.text)
                print(elementos.tag, elementos.text)

                invoice_detail = InvoiceDetail(
                    line=line,
                    code=code,
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    discount=discount,
                    price_without_tax=price_without_tax
                )
                # Recover taxes
                if elementos.tag == 'impuestos':
                    tax_detail = []
                    for impuestos in elementos:
                        impuesto_children = impuestos.getchildren()
                        tax = Tax()
                        for impuesto in impuesto_children:
                            if impuesto.tag == 'codigo':
                                tax.code = impuesto.text
                            if impuesto.tag == 'codigoPorcentaje':
                                tax.code_percent = impuesto.text
                            if impuesto.tag == 'tarifa':
                                tax.tariff = impuesto.text
                            if impuesto.tag == 'baseImponible':
                                tax.base_value = impuesto.text
                            if impuesto.tag == 'valor':
                                tax.value = impuesto.text
                        tax_detail.append(tax)
                    invoice_detail.tax = tax_detail

            new_receipt.invoice_detail.append(invoice_detail)
            line += 1

        db.session.add(new_receipt)
        db.session.commit()

