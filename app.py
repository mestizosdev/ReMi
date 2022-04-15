# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

# Routes
from routes.router import define_routers

define_routers()

