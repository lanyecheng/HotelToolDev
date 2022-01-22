#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
import os.path
import xlwt

from xmind2case.utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to Htp testcase xlsx file 
"""

def set_excel_style():
    """设置表格的样式"""

    # 设置字体
    font = xlwt.Font()
    font.name = 'Microsoft YaHei'
    font.height = 20 * 12

    # 设置边框
    border = xlwt.Borders()
    border.left = 1
    border.right = 1
    border.top = 1
    border.bottom = 1

    # 设置对齐方式
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x01
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x00

    # 初始化样式
    style = xlwt.XFStyle()
    style.font = font
    style.borders = border
    style.alignment = alignment
    style.alignment.wrap = 1

    return style


def xmind_to_htp_xlsx_file(xmind_file):
    """Convert XMind fie to Htp testcase xlsx file """
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to htp file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)
    # print('testcases', testcases)

    fileheader = ['用例编号', '用例树目录', '用例名称', '摘要', '前置条件', '测试步骤', '预期结果', '用例等级', '自动化覆盖', '状态', '用例类型']
    htp_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        htp_testcase_rows.append(row)

    # 设置文件名称地址信息
    htp_file = xmind_file[:-6] + '.xls'
    # 如果文件存在则删除
    if os.path.exists(htp_file):
        os.remove(htp_file)

    # 创建 workbook 对象
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个 sheet 对象
    mysheet = workbook.add_sheet('test')

    # 设置单元格列宽
    mysheet.col(0).width = 256 * 20
    mysheet.col(1).width = 256 * 30
    mysheet.col(2).width = 256 * 45
    mysheet.col(3).width = 256 * 15
    mysheet.col(4).width = 256 * 25
    mysheet.col(5).width = 256 * 55
    mysheet.col(6).width = 256 * 75
    mysheet.col(7).width = 256 * 10
    mysheet.col(8).width = 256 * 15
    mysheet.col(9).width = 256 * 10
    mysheet.col(10).width = 256 * 30

    # 设置冻结为真
    mysheet.set_panes_frozen('1')
    # 水平冻结
    mysheet.set_horz_split_pos(1)

    mystyle = set_excel_style()
    for row, scores in enumerate(htp_testcase_rows):
        for cols, score in enumerate(scores):
            mysheet.write(row, cols, score, mystyle)

    logging.info('Convert XMind file(%s) to a htp csv file(%s) successfully!', xmind_file, htp_file)
    # 保存文件
    workbook.save(htp_file)
    return htp_file


def xmind_to_htp_preview(xmind_file):
    """Convert XMind fie to Htp testcase xlsx file """
    xmind_file = get_absolute_path(xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)
    fileheader = ['用例编号', '用例树目录', '用例名称', '摘要', '前置条件', '测试步骤', '预期结果', '用例等级', '自动化覆盖', '状态', '用例类型']
    htp_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        htp_testcase_rows.append(row)
    return htp_testcase_rows


def gen_a_testcase_row(testcase_dict):
    case_number = ''
    case_tree = get_case_module(testcase_dict['product']) + '~' +get_case_module(testcase_dict['suite'])
    case_title = testcase_dict['name']
    case_summary = ''
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_apply_phase = ''
    case_state = ''
    case_type = gen_case_type(testcase_dict['execution_type'])
    row = [case_number, case_tree, case_title, case_summary, case_precontion, case_step, case_expected_result, case_priority, case_apply_phase, case_state, case_type]
    return row

def get_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''
    for step_dict in steps:
        case_step += step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += step_dict['expectedresults'].replace('\n', '').strip() + '\n'
        # if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: 'P1', 2: 'P2', 3: 'P3'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 'P2'


def gen_case_type(case_type):
    mapping = {1: '回归用例', 2: '回归用例、冒烟用例'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '回归用例'
