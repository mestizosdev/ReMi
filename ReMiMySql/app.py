# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].format(
    os.getenv('DB_USER', 'remi'),
    os.getenv('DB_PASSWORD', 'No_piratear1'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', '3306'),
    os.getenv('DB_NAME', 'remi')
)
db = SQLAlchemy(app)

from models.models import *

migrate = Migrate(app, db)
# Routes
from routes.router import define_routers

define_routers()

# Logger
from utils.logger import define_logger

define_logger()
