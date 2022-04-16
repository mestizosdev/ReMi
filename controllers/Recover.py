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
        is_success, content_str = client.download(access_key)

        if not is_success:
            return {'message': content_str}, 404

        authorized_file = AuthorizedFile()
        authorized_file.save(content_str, access_key)

        return {'Recover': 'In progress'}
