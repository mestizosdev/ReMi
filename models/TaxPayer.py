# -*- coding: utf-8 -*-
from app import db


class TaxPayer(db.Model):
    __tablename__ = 'remi_taxpayers'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    identification = db.Column(db.String, nullable=False)
    business_name = db.Column(db.String, nullable=False)
    trade_name = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    observation = db.Column(db.String)

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
