#!/usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import json
import requests
import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://10.13.2.133:6101/v1/resop/vm/vm_info/'
headers = {'Content-Type':'application/json'}
def get_num():
    csvfile_three = open('1.csv','r')#打开CSV文件
    vm_reader = csv.reader(csvfile_three)
    customer_list_no = []
    split_customer = []
    for vm_row in vm_reader:
        for vm_list in vm_row:
            customer_list = vm_list.split(';')
            customer_list_no.append(customer_list[0])
            split_customer.append(vm_list.split(';'))
    csvfile_three.close()
    return customer_list_no

def write_csv(customer_list_no):
    split_customer = []
    csvfile_four = open('csvtest1.csv', 'wb')#打开csv文件
    subkey_two = ['objName.keyword','parentName.keyword','objStatus.keyword','customer_contacts','customer_email','public_ip',  'customer_mobile','private_ip','customer_name','备注']#提取关键信息，在新的vm名称中，不需要这个操作
    subkey_three = ['customer_contacts','customer_email','public_ip',  'customer_mobile','private_ip','customer_name']
    writer = csv.DictWriter(csvfile_four, fieldnames=subkey_two)#用字典的方式写入
    csvfile_four.write(codecs.BOM_UTF8)
    writer.writeheader()
    header_list = ['objName.keyword','parentName.keyword','objStatus.keyword']
    csvfile_three = open('1.csv','r')#打开CSV文件
    vm_reader = csv.reader(csvfile_three)
    for vm_row in vm_reader:
        for vm_list in vm_row:
            split_customer.append(vm_list.split(';'))
    for a in range(2,len(customer_list_no[3:])):
        zip_dict = dict(map(lambda x,y:[x,y],header_list,split_customer[a][:2]))
        list_num = split_customer[a][0].split(';')
        t = {'vm_name':list_num[0]}#遍历获取的客户编码，将获取的客户编码放到t
        body = json.dumps(t)
        response = requests.post(url=url, data=body, headers=headers)#通过response获取vm信息
        file_text = response.json()
        if file_text['code'] == '0000':
            file_text_vm = file_text['data']#获取vm信息
            new_dic = dict([(key,file_text_vm[key]) for key in subkey_three])#将关键信息放到新的字典new_dic中
            dict_sum = dict(new_dic.items()+zip_dict.items())
            writer.writerow(dict_sum)#将新的字典的信息写入到csv中
        elif file_text['code'] == '20101':
            errmsg = file_text['message']
            zip_dict['备注'] = '%s'%errmsg
            writer.writerow(zip_dict)

if __name__ == '__main__':
    cus = get_num()
    write_csv(cus)

