# -*- coding: utf-8 -*-
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

        for child in object_receipt.find('infoTributaria'):
            print(child.tag, child.text)

        for child in object_receipt.find('infoFactura'):
            print(child.tag, child.text)

        detalles = object_receipt.iter("detalle")

        for detalle in detalles:
            detalle_children = detalle.getchildren()

            for elementos in detalle_children:
                print(elementos.tag, elementos.text)
