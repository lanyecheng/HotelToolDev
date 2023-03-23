#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
import os
from app import app
from flask import render_template, request, url_for, redirect, send_from_directory, g, abort
from os.path import join, exists, basename
from app.datarecord import insert_record, get_records, delete_record
from xmind2case.xmind2htp import xmind_to_htp_preview, xmind_to_htp_xlsx_file
from xmind2case.utils import get_xmind_testsuites


def save_file(file):
    """保存文件数据"""
    if file and allowed_file(file.filename):
        # 这里判断以下 uploads 文件夹是否存在，如果不存在创建
        if not exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        filename = file.filename
        upload_to = join(app.config['UPLOAD_FOLDER'], filename)
        if exists(upload_to):
            filename = '{}_{}.xmind'.format(filename[:-6], arrow.now().strftime('%Y%m%d_%H%M%S'))
            upload_to = join(app.config['UPLOAD_FOLDER'], filename)

        file.save(upload_to)
        insert_record(filename)
        return filename


def allowed_file(filename):
    """判断文件类型"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def delete_row(filename, record_id):
    """数据库逻辑删除"""
    xmind_file = join(app.config['UPLOAD_FOLDER'], filename)
    htp_file = join(app.config['UPLOAD_FOLDER'], filename[:-5] + 'xls')
    for f in [xmind_file, htp_file]:
        if exists(f):
            os.remove(f)
    delete_record(record_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    g.invalid_files = []
    g.filename = None
    g.error = None

    if request.method == 'POST':
        file = request.files['file']

        g.filename = save_file(file)
        # verify_uploaded_files([file])
    if g.filename:
        return redirect(url_for('preview', filename=g.filename))
    else:
        return render_template('index.html', records=list(get_records()))


@app.route('/preview/<filename>')
def preview(filename):
    """预览展示"""
    full_path = join(app.config['UPLOAD_FOLDER'], filename)
    if not exists(full_path):
        abort(404)

    testsuites = get_xmind_testsuites(full_path)
    suite_count = 0
    for suite in testsuites:
        suite_count += len(suite.sub_suites)

    testcases = xmind_to_htp_preview(full_path)
    print(testcases)
    return render_template('preview2.html', name=filename, suite=testcases, suite_count=suite_count)


@app.route('/delete_file/<filename>/<int:record_id>')
def delete_file(filename, record_id):
    """删除文件"""
    full_path = join(app.config['UPLOAD_FOLDER'], filename)
    if not exists(full_path):
        abort(404)
    else:
        delete_row(filename, record_id)
    return redirect(url_for('index'))


@app.route('/to/htp/<filename>')
def download_xmind_htp(filename):
    """下载表格数据"""
    full_path = join(app.config['UPLOAD_FOLDER'], filename)
    print(full_path)
    if not exists(full_path):
        abort(404)
    htp_file = xmind_to_htp_xlsx_file(full_path)
    filename = basename(htp_file)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/test')
def test():
    # return render_template('index.html')
    return render_template('base.html')



