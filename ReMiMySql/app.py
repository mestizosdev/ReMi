# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import utils.config

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.cfg')
app = utils.config.vars_config(app=app)

db = SQLAlchemy(app)

from models.models import *

migrate = Migrate(app, db)
# Routes
from routes.router import define_routers

define_routers()

# Logger
from utils.logger import define_logger

define_logger()
