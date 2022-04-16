# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import ForeignKey, DateTime


class InvoiceDetail(db.Model):
    __tablename__ = 'remi_invoices_details'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    receipt_id = db.Column(db.Integer, ForeignKey('remi_receipts.id'))
    line = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(280), nullable=False)
    description = db.Column(db.String(280), nullable=False)
    quantity = db.Column(db.String(280), nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)
    discount = db.Column(db.Numeric, nullable=False)
    price_without_tax = db.Column(db.Numeric, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
