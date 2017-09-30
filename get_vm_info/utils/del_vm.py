#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import
import traceback
import csv
import sys
import json
import requests
import codecs
import xlrd

from get_vm_info import logger_config, VMINFO_URL, GET_CUSTOMER_BYNO_URL
logger = logger_config('del_vm', 'vminfo.log')

reload(sys)
sys.setdefaultencoding('utf-8')


def read_csv(file_name):
    '''
        读取原始csv文件，获取vm相关信息，并返回一个字典数据
    :return: vm_info list
    '''
    vm_info = {}
    try:
        f = open('%s' % file_name, 'r')
        logger.info('Start reading upload file:%s' % f)
        # 去除带有‘sep’的行和首行
        rows = f.readlines()[2:]
        # 以';'切割数据
        rows_list = [row.split(';') for row in rows]
        for row in rows_list:
            vmname = row[0]
            host = row[1]
            status = row[2]
            vm_info[vmname] = {"host": host, "status": status}
        f.close()
        return vm_info
    except Exception:
        logger.info(traceback.format_exc())
        return vm_info


def read_from_xlsx(file_name):
    workbook_xlsx = xlrd.open_workbook('%s' % file_name,'r')
    sheetnames = workbook_xlsx.sheet_names()
    sheet = workbook_xlsx.sheet_by_name(sheet_name=sheetnames[0])
    msg = []
    for row in range(sheet.nrows):
        msg.append(sheet.cell(row, 0).value)
    return msg


def get_vminfo_byname(vm_name):
    """
        根据vm名称, 从api接口获取相关信息
    :return: vm info data:e.g.: {'host': 'xxx'}
    """
    headers = {'Content-Type': 'application/json'}
    data = {"vm_name": vm_name}
    post_data = json.dumps(data)
    results = requests.post(
        url=VMINFO_URL, headers=headers, data=post_data).json()
    logger.info('VM信息获取结果:%s' % results.get("code_msg"))
    if results.get("code_msg") == "success":
        vm_data = results.get('data')
        vm_data['comment'] = 'ok'
        return vm_data
    # 数据异常时,只返回客户信息
    message = results.get("message")
    vm_data = get_customer_info(vm_name)
    vm_data['comment'] = message
    logger.warn('VM:%s只返回客户信息' % vm_name)
    return vm_data


def write_to_csv(vm_info, filename):
    '''
        根据获取的vm_info信息，写入csv文件,并以当前时间为后缀命名
    :data: vm_info data
    :return: csv file
    '''
    try:
        file = open(filename, 'wb')
        file.write(codecs.BOM_UTF8)
        writer = csv.writer(file)
        title_row = ['VM名称', '宿主机', '状态', '客户名称',
                     '联系人', '手机号', '邮箱地址', '公网地址', '私网地址', '备注']
        writer.writerow(title_row)
        for key, value in vm_info.iteritems():
            vm_name = key
            host = value.get('host')
            status = value.get('status')
            customer_name = value.get('customer_name')
            customer_contacts = value.get('customer_contacts')
            customer_mobile = value.get('customer_mobile')
            customer_email = value.get('customer_email')
            public_ip = value.get('public_ip')
            private_ip = value.get('private_ip')
            comment = value.get('comment')
            row_vm_data = [vm_name, host, status, customer_name, customer_contacts,
                           customer_mobile, customer_email, public_ip, private_ip, comment]
            writer.writerow(row_vm_data)
        file.close()
    except Exception:
        logger.warn(traceback.format_exc())


def get_customer_info(vm_name):
    """
        根据vm名称手动截取‘-’前的第一个字段为客户编号,并根据客户编号,查询客户信息
    :return: customer info values 客户信息
    """
    cst_values = {}
    customer_no = vm_name.split('-')[0]
    headers = {'Content-Type': 'application/json'}
    csm_data = {"customerNo": customer_no}
    post_csm_data = json.dumps(csm_data)
    logger.info("Get customer info by customerNo start...")
    response = requests.post(url=GET_CUSTOMER_BYNO_URL,
                             data=post_csm_data, headers=headers).json()
    logger.info("Get customer info by customerNo end...")
    cst_infos = response.get('customer')
    cst_values['customer_name'] = cst_infos.get('customerName')
    cst_values['customer_contacts'] = cst_infos.get('operateContact')
    cst_values['customer_mobile'] = cst_infos.get('contactPhone')
    cst_values['customer_email'] = cst_infos.get('contactEmail')
    logger.info("customer info is %s" % cst_values)
    return cst_values
