# -*- coding: utf-8 -*-
from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        return {
            'application': {'name': 'Recover my receipt'},
            'success': True
        }
