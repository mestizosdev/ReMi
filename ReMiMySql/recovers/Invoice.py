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

        details = object_receipt.iter("detalle")

        line = 1
        for detail in details:
            children_detail = detail.getchildren()
            invoice_detail = None

            code = None
            description = None
            quantity = 0.0
            unit_price = 0.0,
            discount = 0.0,
            price_without_tax = 0.0

            for element_tax in children_detail:
                if element_tax.tag == 'codigoPrincipal':
                    code = element_tax.text
                if element_tax.tag == 'descripcion':
                    description = element_tax.text
                if element_tax.tag == 'cantidad':
                    quantity = float(element_tax.text)
                if element_tax.tag == 'precioUnitario':
                    unit_price = float(element_tax.text)
                if element_tax.tag == 'descuento':
                    discount = float(element_tax.text)
                if element_tax.tag == 'precioTotalSinImpuesto':
                    price_without_tax = float(element_tax.text)
                print(element_tax.tag, element_tax.text)

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
                if element_tax.tag == 'impuestos':
                    tax_detail = []
                    for taxes_details in element_tax:
                        tax_children = taxes_details.getchildren()
                        tax = Tax()
                        for tax_element in tax_children:
                            if tax_element.tag == 'codigo':
                                tax.code = tax_element.text
                            if tax_element.tag == 'codigoPorcentaje':
                                tax.code_percent = tax_element.text
                            if tax_element.tag == 'tarifa':
                                tax.tariff = tax_element.text
                            if tax_element.tag == 'baseImponible':
                                tax.base_value = tax_element.text
                            if tax_element.tag == 'valor':
                                tax.value = tax_element.text
                        tax_detail.append(tax)
                    invoice_detail.tax = tax_detail

            new_receipt.invoice_detail.append(invoice_detail)
            line += 1

        db.session.add(new_receipt)
        db.session.commit()
