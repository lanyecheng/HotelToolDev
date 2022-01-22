#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from app import app, db


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        # 删除表及数据
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')