# -*- coding: utf-8 -*-
from app import db


class TaxPayer(db.Model):
    __tablename__ = 'remi_taxpayers'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    identification = db.Column(db.String(280), nullable=False)
    business_name = db.Column(db.String(280), nullable=False)
    trade_name = db.Column(db.String(280))
    address = db.Column(db.String(280), nullable=False)
    status = db.Column(db.String(280), nullable=False)

    def __init__(self,
                 identification,
                 business_name,
                 address,
                 trade_name=None,
                 status='Activo'):
        self.identification = identification,
        self.business_name = business_name,
        self.trade_name = trade_name,
        self.address = address,
        self.status = status,
