# -*- coding: utf-8 -*-
from flask_restful import Resource
from utils.AccessKey import AccessKey
from utils.HttpClient import HttpClient
from utils.AuthorizedFile import AuthorizedFile


class Recover(Resource):
    @classmethod
    def get(cls, access_key):
        if not AccessKey.is_valid(access_key):
            return {'message': 'Clave de acceso no valida'}, 422

        client = HttpClient()
        is_success, content = client.download(access_key)

        if not is_success:
            return {'message': content.status}, 404

        authorized_file = AuthorizedFile()
        type_receipt, object_receipt = authorized_file.save(content.receipt, access_key)

        return {'Recover': 'In progress'}
