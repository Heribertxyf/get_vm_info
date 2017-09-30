#!/usr/bin/env python
# coding:utf-8
import csv
import json
import requests
import codecs


def read_csv(file_name):
    '''
    从原始的csv文件中提取客户编号并返回所有提取的客户编号。
    customer_no 用于保存所有的客户编号
    every_line_in_original_csv 保存文件中每一行的信息
    splited_original_msg 将信息以;分割，从而提取原始信息。
    :param file_name: 原始.csv文件名称(例'grafana_data_export.csv')
    :return: customer_no, every_line_in_original_csv
    '''
    customer_no = []
    every_line_in_original_csv = []
    try:
        f = open('%s' % file_name, 'r')
        reader = csv.reader(f)
        for row in reader:
            every_line_in_original_csv.extend(row)                              # 原始文件的每一行的信息
            splited_original_msg = row[0].split(';')                            # 以‘;’分割，获取用户编号
            customer_no.append(splited_original_msg[0])                         # 将所有的客户编号保存到customer_no中
    except:
        print("The original csv file can't be operated.")
    else:
        f.close()
    return (customer_no[2:], every_line_in_original_csv)


def post_request(customer_no):
    '''
    url是API端口地址，header是头信息，data是体信息
    :param customer_no: 从原始文件中提取的所有VM名称
    :return: customer_message：获取到的所有VM的客户信息
    '''
    url = 'http://10.13.2.133:6101/v1/resop/vm/vm_info/'
    headers = {'Content-Type': 'application/json'}
    final_msg = []
    dic_name = 'data'
    for one_no in customer_no:
        data = {"vm_name": "%s" % one_no}
        data = json.dumps(data)                                                 #使data变为json格式
        r = requests.post(url=url, data=data, headers=headers)
        get_msg = r.json()                                                      #get_msg是获取信息，字典格式
        if get_msg['code'] == '0000':                                           #对请求结果进行判断，成功则获取客户名称，客户级别，联系人姓名，联系人电话，联系人邮箱>，运维联系人，销售信息
            customer_name = get_msg[dic_name]['customer_name']
            contact_name = get_msg[dic_name]['customer_contacts']
            contact_phone = get_msg[dic_name]['customer_mobile']
            contact_email = get_msg[dic_name]['customer_email']
            public_ip = get_msg[dic_name]['public_ip']
            private_ip = get_msg[dic_name]['private_ip']
            final_msg.append([customer_name, contact_name, contact_phone, contact_email, public_ip, private_ip, ''])
        else:                                                                   #若失败，获取失败信息，并记录在备注。
            errmsg = get_msg['message'] + get_msg['code_msg']
            final_msg.append(['', '', '', '', '', '', errmsg])
    return final_msg


def write_to_csv(save_addr, every_line, post_msg):
    '''
    对csv文件的写入采取的是按行写入的方式。msg是每一行的完整信息。
    :param save_addr: The new .csv file address
    :param every_line: every_line_message in original file
    '''
    write_file = open('%s' % save_addr, 'w', newline='')
#    write_file.write(codecs.BOM_UTF8)
    title = ['objName.keyword', 'parentName.keyword', 'objStatus.keyword','客户名称', '联系人姓名', '联系人电话', '联系人邮件',
             '公网IP', '私网IP', '备注']
    spamwriter = csv.writer(write_file)
    spamwriter.writerow(title)
    for i in range(len(post_msg)):
        msg = []
        msg.extend(every_line[i+2].split(';'))                                  #获取原始文件中的信息并进行分隔
        del msg[-1]
        msg.extend(post_msg[i])                                                 #扩充msg信息，将所有得到的每一台VM的信息保存在msg中。
        spamwriter.writerow(msg)                                                #按行写入csv
    write_file.close()

if __name__ == "__main__":
    (customer_id, everyline) = read_csv('now.csv')
    final_message = post_request(customer_id)
    write_to_csv('1111.csv', everyline, final_message)
