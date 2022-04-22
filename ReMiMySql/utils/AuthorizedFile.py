# -*- coding: utf-8 -*-
import os
from utils.AccessKey import AccessKey
import xml.etree.ElementTree as ParseXml


class AuthorizedFile(object):
    path_received = None

    def __init__(self):
        self.path_received = '/app/ReMi/received'

    def save(self, content_str, access_key):
        path_xml = self.path_received + os.sep + access_key + '.xml'
        print("Path of XML: " + path_xml)
        file = open(path_xml, "w")
        file.write(content_str)
        file.close()
        self.clean(path_xml)
        type_receipt = AccessKey.document_type(access_key)
        return type_receipt, path_xml

    def clean(self, file_xml):
        """
        Clean blank spaces in xml file_xml
        """
        clean_lines = []
        with open(file_xml, 'r', encoding='utf8') as f:
            lines = f.readlines()
            clean_lines = [l.strip() for l in lines if l.strip()]
        with open(file_xml, 'w', encoding='utf8') as f:
            f.writelines('\n'.join(clean_lines))
        f.close
    
    def xml_to_object(self, file_xml):
        tree = ParseXml.parse(file_xml)
        root_receipt = tree.getroot()

        return root_receipt

