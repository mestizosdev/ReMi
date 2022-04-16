# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import ForeignKey, DateTime


class Invoice(db.Model):
    __tablename__ = 'remi_invoices'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    taxpayer_id = db.Column(db.Integer, ForeignKey('remi_taxpayers.id'))
    access_key = db.Column(db.String, nullable=False, unique=True)
    establishment = db.Column(db.String, nullable=False)
    emission_point = db.Column(db.String, nullable=False)
    sequence = db.Column(db.String, nullable=False)
    date_emission = db.Column(DateTime(), nullable=False)
    authorization = db.Column(db.String)
    date_authorization = db.Column(DateTime())
    receptor_identification = db.Column(db.String)
    receptor_business_name = db.Column(db.String)
    total = db.Column(db.Numeric, nullable=False)

    def __init__(self,
                 identification,
                 business_name,
                 address,
                 trade_name=None,
                 status='Activo',
                 observation=None):
        self.identification = identification,
        self.business_name = business_name,
        self.trade_name = trade_name,
        self.address = address,
        self.status = status,
        self.observation = observation