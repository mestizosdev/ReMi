# -*- coding: utf-8 -*-
from app import api, app

from controllers.index import *
from controllers.version import *
from controllers.recover import *


def define_routers():
    api.add_resource(Recover, '/recover/<string:access_key>')
    api.add_resource(Index, '/')
    api.add_resource(Version, '/version')
