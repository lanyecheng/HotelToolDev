#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from datetime import datetime


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    note = db.Column(db.Text)
    create_on = db.Column(db.DateTime, default=datetime.now())
    is_deleted = db.Column(db.Integer, default=0)
