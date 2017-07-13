# !usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import codecs
import json
import requests
import argparse


def read_csv(file_name):
    customor_no = []
    f = codecs.open('%s' % file_name, 'r')
    reader = csv.reader(f)
    for row in reader:
        every_line_in_original_csv.append(row[0])
        splited_original_msg.append(row[0].split('-'))
    for z in range(len(splited_original_msg)-2):
        customor_no.append(splited_original_msg[z + 2][0])
    f.close()
    return customor_no


def post_request(customer_no):
    url = 'http://10.13.2.235:6003/customer/getCustomerByNo'
    headers = {'Content-Type': 'application/json'}
    data = {"customerNo": "%s" % customer_no}
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    get_msg = r.json()
    final_msg = []
    if get_msg['status'] == 'success':
        customer_name = get_msg['customer']['customerName']
        level = get_msg['customer']['level']
        contact_name = get_msg['customer']['contactName']
        operate_contact = get_msg['customer']['operateContact']
        contact_phone = get_msg['customer']['contactPhone']
        contact_email = get_msg['customer']['contactEmail']
        sale_name = get_msg['customer']['sale_name']
        final_msg = [customer_name, level, contact_name, contact_phone, contact_email, operate_contact, sale_name, '']
    elif get_msg['status'] == 'failure':
        errmsg = get_msg['errMsg']
        final_msg = ['', '', '', '', '', '', '', errmsg]
    return final_msg


def write_to_csv():
    write_file = codecs.open('final.csv', 'w', 'utf_8_sig')
    title = ['objName.keyword', 'parentName.keyword', 'objStatus.keyword', '客户名称', '级别', '联系人姓名', '联系人电话', '联系人邮件',
             '运维联系人姓名', '销售姓名', '备注']
    spamwriter = csv.writer(write_file)
    spamwriter.writerow(title)
    for i in range(len(customor_id)):
        try:
            post_msg = post_request(customor_id[i])
        except:
            error_id.append(customor_id[i])
        else:
            msg = []
            msg.extend(every_line_in_original_csv[i + 2].split(';'))
            del msg[-1]
            msg.extend(post_msg)
            spamwriter.writerow(msg)
    if len(error_id) == 1:
        error_id.append(u'无')
        spamwriter.writerow(error_id)
    else:
        spamwriter.writerow(error_id)
    write_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--address", nargs='?', help="original file address.")
    args = parser.parse_args()
    original_file_addr = args.address
    original_file_name = '%s' % original_file_addr[0]
    splited_original_msg = []
    every_line_in_original_csv = []
    error_id = ['进程出错客户编码']
    customor_id = read_csv(original_file_name)
    write_to_csv()
