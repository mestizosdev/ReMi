# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import ForeignKey


class Tax(db.Model):
    __tablename__ = 'remi_taxes'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    invoice_detail_id = db.Column(db.Integer, ForeignKey('remi_invoices_details.id', ondelete='CASCADE'))
    code = db.Column(db.String(280), nullable=False)
    code_percent = db.Column(db.String(280), nullable=False)
    tariff = db.Column(db.Numeric(30, 6), nullable=False)
    base_value = db.Column(db.Numeric(30, 6), nullable=False)
    value = db.Column(db.Numeric(30, 6), nullable=False)

    def __init__(self,
                 code,
                 code_percent,
                 tariff,
                 base_value,
                 value):
        self.code = code,
        self.code_percent = code_percent,
        self.tariff = tariff,
        self.base_value = base_value
        self.value = value
