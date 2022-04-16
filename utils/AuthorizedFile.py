# -*- coding: utf-8 -*-
import os
from utils.AccessKey import AccessKey
import xml.etree.ElementTree as parsexml


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
        return self.xml_to_object(access_key, path_xml)

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
    
    def xml_to_object(self, access_key, file_xml):
        type = AccessKey.document_type(access_key)
        tree = parsexml.parse(file_xml)
        root = tree.getroot()

        return type, root

