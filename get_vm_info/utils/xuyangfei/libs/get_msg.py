# -*- coding:utf-8 -*-
from libs.operate_DB import final
from front.__init__ import db

def get_all_place(session):
    '''
    从数据库中获取源，目的，权值
    :param session:数据库会话
    :return:所有的位置名（类型：list）， 点到点对应权值（类型：dict）
    '''
    all_db_place = []
    all_place = []
    r_dict = {}
    for S, D, W in session.query(final.Source, final.Destination, final.Weight):
        all_db_place.append(S)
        all_db_place.append(D)
        r_name = S + '_to_' + D
        r_dict[r_name] = W
        d_name = D + '_to_' + S
        r_dict[d_name] = W
    for i in all_db_place:
        if all_place.count(i) == 0:
            all_place.append(i)
    return (all_place, r_dict)


def transmit_to_homepage():
    '''
    获得页面展示的列表
    :return: 页面列表（类型：list）
    '''
    (all_place_x, weight_dict) = get_all_place(db.session)
    row_0 = ['']
    row_0.extend(all_place_x)
    data_deal = []
    for i in range(len(row_0)):
        data_deal.append([])
        data_deal[i].append(row_0[i])
    data_deal[0] = row_0
    for r in range(1, len(data_deal[0])):
        for c in range(1, len(data_deal)):
            if data_deal[0][r] == data_deal[c][0]:
                data_deal[c].append('')
            else:
                try:
                    data_deal[c].append(weight_dict[data_deal[0][r] + '_to_' + data_deal[c][0]])
                except KeyError:
                    data_deal[c].append('')
    return data_deal