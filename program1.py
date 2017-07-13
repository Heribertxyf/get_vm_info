# !usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import codecs
import json
import requests
import argparse


def read_csv(file_name):
    '''
    从原始的csv文件中提取客户编号并返回所有提取的客户编号。
    customer_id 用于保存所有的客户编号
    every_line_in_original_csv 保存文件中每一行的信息
    splited_original_msg将信息以-分割，从而提取客户编号
    '''
    customer_no = []
    splited_original_msg = []
    every_line_in_original_csv = []
    f = open('%s' % file_name, 'r')
    reader = csv.reader(f)
    for row in reader:
        every_line_in_original_csv.append(row[0])                 #原始文件的每一行的信息
        splited_original_msg.append(row[0].split('-'))            #以‘-’分割，获取用户编号，新的API用VM名称进行查询就不需要这步。
    for z in range(len(splited_original_msg)-2):
        customer_no.append(splited_original_msg[z + 2][0])         #除去两行标题，将所有的客户编号保存到customer_no中
    f.close()
    return (customer_no, every_line_in_original_csv)


def post_request(customer_no):
    '''
    url是API端口地址，header是头信息，data是体信息

    '''
    url = 'http://10.13.2.235:6003/customer/getCustomerByNo'
    headers = {'Content-Type': 'application/json'}
    data = {"customerNo": "%s" % customer_no}
    data = json.dumps(data)                                                 #使data变为json格式
    r = requests.post(url=url, data=data, headers=headers)
    get_msg = r.json()                                                      #get_msg是获取信息，字典格式
    final_msg = []
    if get_msg['status'] == 'success':              #对请求结果进行判断，成功则获取客户名称，客户级别，联系人姓名，联系人电话，联系人邮箱，运维联系人，销售信息
        customer_name = get_msg['customer']['customerName']
        level = get_msg['customer']['level']
        contact_name = get_msg['customer']['contactName']
        operate_contact = get_msg['customer']['operateContact']
        contact_phone = get_msg['customer']['contactPhone']
        contact_email = get_msg['customer']['contactEmail']
        sale_name = get_msg['customer']['sale_name']
        final_msg = [customer_name, level, contact_name, contact_phone, contact_email, operate_contact, sale_name, '']
    elif get_msg['status'] == 'failure':            #若失败，获取失败信息，并记录在备注。
        errmsg = get_msg['errMsg']
        final_msg = ['', '', '', '', '', '', '', errmsg]
    return final_msg


def write_to_csv(save_addr, every_line):
    '''
    先对结果文件写入第一行标题，for循环对每一个获取到的客户编号调用post_request，
    进程失败的记录在error_id中并在文件的最后一行显示。
    对csv文件的写入采取的是按行写入的方式。msg是每一行的完整信息。
    '''
    write_file = open('%s' % save_addr, 'w', newline="")
    title = ['objName.keyword', 'parentName.keyword', 'objStatus.keyword', '客户名称', '级别', '联系人姓名', '联系人电话', '联系人邮件',
             '运维联系人姓名', '销售姓名', '备注']
    spamwriter = csv.writer(write_file)
    spamwriter.writerow(title)
    error_id = ['进程出错客户编码']
    for i in range(len(customor_id)):
        try:
            post_msg = post_request(customor_id[i])
        except:
            error_id.append(customor_id[i])
        else:
            msg = []
            msg.extend(every_line[i + 2].split(';'))                 #获取原始文件中的信息并进行分隔
            del msg[-1]
            msg.extend(post_msg)                                      #扩充msg信息，将所有得到的每一台VM的信息保存在msg中。
            spamwriter.writerow(msg)                                  #按行写入csv
    if len(error_id) == 1:                                            #若有进程失败的vm，记录在最后一行
        error_id.append(u'无')
        spamwriter.writerow(error_id)
    else:
        spamwriter.writerow(error_id)
    write_file.close()


if __name__ == '__main__':
    '''
    根据用户输入的命令行参数得到初始文件地址，并进而进行处理。
    用户命令：python program1.py -d "file.csv -s "final_mag.csv"
    获取客户信息的过程为，先对初始文件进行信息处理read_csv得到客户编号，
    在write_to_csv中调用post_request进行http请求，获得客户信息，
    然后按行写入csv文件。
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--address", nargs='*', help="original file address.")
    parser.add_argument("-s", "--save", nargs='*', help="save file address.", default="final_msg.csv")
    args = parser.parse_args()
    original_file_addr = args.address[0]
    save_file_addr = args.save[0]
    original_file_name = '%s' % original_file_addr
    (customor_id, every) = read_csv(original_file_name)
    write_to_csv(save_file_addr, every)
