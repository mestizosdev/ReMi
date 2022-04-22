# -*- coding: utf-8 -*-


class StatusReceipt(object):
    access_key = None
    authorization = None
    authorization_date = None
    status = None
    receipt = None

    def __init__(self):
        self.access_key = ''
        self.authorization = ''
        self.authorization_date = ''
        self.status = ''
        self.receipt = ''