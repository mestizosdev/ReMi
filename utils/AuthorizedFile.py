# -*- coding: utf-8 -*-
import os


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
