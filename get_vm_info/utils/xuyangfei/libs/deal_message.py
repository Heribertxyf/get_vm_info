#!/usr/bin/env python
#coding:utf-8
import csv
import json
import requests
import codecs


def read_csv(file_name):
    '''
    从原始的csv文件中提取客户编号并返回所有提取的客户编号。
    customer_id 用于保存所有的客户编号
    every_line_in_original_csv 保存文件中每一行的信息
    splited_original_msg将信息以-分割，从而提取客户编号
    :param file_name: original .csv file_name('grafana_data_export.csv')
    :return: customer_id
    '''
    customer_no = []
    every_line_in_original_csv = []
    try:
        f = open('%s' % file_name, 'r')
        reader = csv.reader(f)
        for row in reader:
            every_line_in_original_csv.extend(row)  # 原始文件的每一行的信息
            splited_original_msg = row[0].split(';')  # 以‘;’分割，获取用户编号，新的API用VM名称进行查询就不需要这步。
            customer_no.append(splited_original_msg[0])  # 除去两行标题，将所有的客户编号保存到customer_no中
    except:
        print("The original csv file can't be operated.")
    else:
        f.close()
    return (customer_no[2:], every_line_in_original_csv)


def post_request(customer_no):
    '''
    url是API端口地址，header是头信息，data是体信息
    :param customer_no: customer_id
    :return: customer_message
    '''
    url = 'http://10.13.2.133:6101/v1/resop/vm/vm_info/'
    headers = {'Content-Type': 'application/json'}
    data = {"vm_name": "%s" % customer_no}
    data = json.dumps(data)                                                 #使data变为json格式
    r = requests.post(url=url, data=data, headers=headers)
    get_msg = r.json()                                                      #get_msg是获取信息，字典格式
    final_msg = []
    dic_name = 'data'
    if get_msg['code'] == '0000':              #对请求结果进行判断，成功则获取客户名称，客户级别，联系人姓名，联系人电话，联系人邮箱>，运维联系人，销售信息
        dic_name = 'data'
        customer_name = get_msg[dic_name]['customer_name']
        contact_name = get_msg[dic_name]['customer_contacts']
        contact_phone = get_msg[dic_name]['customer_mobile']
        contact_email = get_msg[dic_name]['customer_email']
        public_ip = get_msg[dic_name]['public_ip']
        private_ip = get_msg[dic_name]['private_ip']
        final_msg = [customer_name, contact_name, contact_phone, contact_email, public_ip, private_ip, '']
    else:                                       #若失败，获取失败信息，并记录在备注。
        errmsg = get_msg['message'] + get_msg['code_msg']
        final_msg = ['', '', '', '', '', '', errmsg]
    return final_msg


def write_to_csv(save_addr, every_line, customer_id):
    '''
    先对结果文件写入第一行标题，for循环对每一个获取到的客户编号调用post_request，
    进程失败的记录在error_id中并在文件的最后一行显示。
    对csv文件的写入采取的是按行写入的方式。msg是每一行的完整信息。
    :param save_addr: The new .csv file address
    :param every_line: every_line_message in original file
    '''
    write_file = open('%s' % save_addr, 'w')
    write_file.write(codecs.BOM_UTF8)
    title = ['objName.keyword', 'parentName.keyword', 'objStatus.keyword','客户名称', '联系人姓名', '联系人电话', '联系人邮件', 
             '公网IP', '私网IP', '备注']
    spamwriter = csv.writer(write_file)
    spamwriter.writerow(title)
    error_id = ['进程出错客户编码']
    for i in range(len(customer_id)):
        try:
            post_msg = post_request(customer_id[i])
        except:
            error_id.append(customer_id[i])
        else:
            msg = []
            msg.extend(every_line[i+2].split(';'))                 #获取原始文件中的信息并进行分隔
            del msg[-1]
            msg.extend(post_msg)                                      #扩充msg信息，将所有得到的每一台VM的信息保存在msg中。
            spamwriter.writerow(msg)                                  #按行写入csv
    if len(error_id) == 1:                                            #若有进程失败的vm，记录在最后一行
        error_id.append(u'无')
        spamwriter.writerow(error_id)
    else:
        spamwriter.writerow(error_id)
    write_file.close()




















































