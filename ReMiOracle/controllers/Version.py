# -*- coding: utf-8 -*-
from flask_restful import Resource
import sys
import platform
from app import db


class Version(Resource):
    @staticmethod
    def get():
        result = db.session.execute('SELECT banner FROM v$version where rownum = 1')
        names = [row[0] for row in result]
        return {
            'versionDatabase': names[0],
            'versionPython': sys.version,
            'versionOS': platform.platform(),
            'version': '0.0.1'
        }
