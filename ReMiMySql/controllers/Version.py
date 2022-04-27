# -*- coding: utf-8 -*-
from flask_restful import Resource
import sys
import platform
import logging

logger = logging.getLogger(__name__)

from app import db


class Version(Resource):
    @staticmethod
    def get():
        try:
            result = db.session.execute('select version() as version')
            names = [row[0] for row in result]
            return {
                'versionDatabase': 'MySql' + ' ' + names[0],
                'versionPython': sys.version,
                'versionOS': platform.platform(),
                'version': '0.0.1'
            }
        except Exception as e:
            logger.error(e)
            return {'message': str(e)}, 501
