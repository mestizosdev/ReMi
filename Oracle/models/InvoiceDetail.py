# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import ForeignKey


class InvoiceDetail(db.Model):
    __tablename__ = 'remi_invoices_details'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    receipt_id = db.Column(db.Integer, ForeignKey('remi_receipts.id', ondelete='CASCADE'))
    line = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(280), nullable=False)
    description = db.Column(db.String(4000), nullable=False)
    quantity = db.Column(db.Numeric(30, 6), nullable=False)
    unit_price = db.Column(db.Numeric(30, 6), nullable=False)
    discount = db.Column(db.Numeric(30, 4), nullable=False)
    price_without_tax = db.Column(db.Numeric(30, 4), nullable=False)

    tax = db.relationship(
        'Tax',
        backref='tax',
        cascade='all, delete')

    def __init__(self,
                 line,
                 code,
                 description,
                 quantity,
                 unit_price,
                 discount,
                 price_without_tax):
        self.line = line
        self.code = code
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount = discount
        self.price_without_tax = price_without_tax
