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

    def __init__(self,
                 taxpayer_id,
                 access_key,
                 type_receipt,
                 establishment,
                 emission_point,
                 sequence,
                 date_emission,
                 authorization,
                 date_authorization,
                 receptor_identification,
                 receptor_business_name,
                 total=0):
        self.taxpayer_id = taxpayer_id
        self.access_key = access_key
        self.type_receipt = type_receipt
        self.establishment = establishment
        self.emission_point = emission_point
        self.sequence = sequence
        self.date_emission = date_emission
        self.authorization = authorization
        self.date_authorization = date_authorization
        self.receptor_identification = receptor_identification
        self.receptor_business_name = receptor_business_name
        self.total = total

