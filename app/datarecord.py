#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from app.models import Records


def insert_record(xmind_name, note=''):
    r1 = Records(title=xmind_name, note=note)
    db.session.add(r1)
    db.session.commit()


def get_records(limit=8):
    short_name_length = 120
    rows = Records.query.order_by(Records.id.desc()).filter(Records.is_deleted != 1).limit(int(limit)).all()
    for row in rows:
        row_id, name, short_name, note, create_on = row.id, row.title, row.title, row.note, row.create_on
        if len(name) > short_name_length:
            short_name = name[:short_name_length] + '...'

        create_on = create_on.strftime('%Y-%m-%d %H:%M:%S')
        yield short_name, name, create_on, note, row_id


def delete_record(record_id):
    row = Records.query.get(record_id)
    row.is_deleted = 1
    db.session.commit()
