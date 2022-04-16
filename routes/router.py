# -*- coding: utf-8 -*-
from app import api, app

from controllers.Index import *
from controllers.Version import *
from controllers.Recover import *


def define_routers():
    api.add_resource(Recover, '/recover/<string:access_key>')
    api.add_resource(Index, '/')
    api.add_resource(Version, '/version')


@app.errorhandler(404)
def invalid_route(e):
    """
        Define custom 404 in json when not exist route
    """
    app.logger.error('Route not found')
    return {'message': 'Route not found ' + str(e)}, 404
