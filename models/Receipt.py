# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import ForeignKey, DateTime


class Receipt(db.Model):
    __tablename__ = 'remi_receipts'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    taxpayer_id = db.Column(db.Integer, ForeignKey('remi_taxpayers.id'))
    access_key = db.Column(db.String(280), nullable=False, unique=True)
    type_receipt = db.Column(db.String(280), nullable=False)
    establishment = db.Column(db.String(280), nullable=False)
    emission_point = db.Column(db.String(280), nullable=False)
    sequence = db.Column(db.String(280), nullable=False)
    date_emission = db.Column(DateTime(), nullable=False)
    authorization = db.Column(db.String(280))
    date_authorization = db.Column(DateTime())
    receptor_identification = db.Column(db.String(280))
    receptor_business_name = db.Column(db.String(280))
    total = db.Column(db.Numeric, nullable=False)