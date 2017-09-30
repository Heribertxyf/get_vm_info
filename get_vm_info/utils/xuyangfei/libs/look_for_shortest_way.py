import networkx
from front.__init__ import db
from libs.operate_DB import *
G = networkx.Graph()


def make_path_beautiful(way):
    '''
    把路径美化
    :param way: 路径（类型：list）
    :return: 美化后路径（类型：str）
    '''
    for i in range(len(way)):
        if i == 0:
            final_shortest_way = way[i]
        else:
            final_shortest_way = final_shortest_way + '-->' + way[i]
    return final_shortest_way


def sort_way(ways, lenths):
    '''
    根据路径的总权值进行排序
    :param ways: 总路径列表（类型：list）
    :param lenths: 每条路径总权值（类型：list）
    :return: 排序后的路径和权值（分别存在列表中）
    '''
    ways_dic = {}
    sorted_lenths = []
    sorted_ways = []
    for i in range(len(ways)):
        ways_dic[ways[i]] = lenths[i]
    sorted_dic = sorted(ways_dic.items(), key=lambda d:d[1])
    need_num = 3
    for num in range(need_num):
        sorted_lenths.append(sorted_dic[num][1])
        sorted_ways.append(sorted_dic[num][0])
    return (sorted_ways, sorted_lenths)


def count_path_weight(all_ways):
    '''
    计算路径总权值
    :param all_ways:所有路径（类型：list）
    :return: 美化后路径和每条路径的权值
    '''
    final_all_ways = []
    each_path_lenth = []
    for each_path in all_ways:
        all_ways_lenth = 0
        for p in range(len(each_path) - 1):
            all_ways_lenth += G.edge[each_path[p]][each_path[p + 1]]['weight']
        each_path_lenth.append(all_ways_lenth)
        final_each_way = make_path_beautiful(each_path)
        final_all_ways.append(final_each_way)
    return (final_all_ways, each_path_lenth)


def get_way(source, destination):
    '''
    先从数据库中提取节点，边，权值，利用networkx获取到源到目的的所有路径及最短路径
    :param source: 源地址（类型：str）
    :param destination: 目的地址（类型：str）
    :return: 最短路径，从源到目的的所有路径及各自路径的总权值
    '''
    for S, D, W in db.session.query(final.Source, final.Destination, final.Weight):
        G.add_edge(S, D, weight=W)

    shortest_way = networkx.all_shortest_paths(G, '%s' % source, '%s' % destination, weight='weight')
    final_shortest_way = []
    for s in shortest_way:
        final_shortest_way.append(make_path_beautiful(s))
    all_ways = networkx.all_simple_paths(G, source, target=destination)
    (ways, lenths) = count_path_weight(all_ways)
    (final_all_ways, each_path_lenth) = sort_way(ways, lenths)
    return final_shortest_way, final_all_ways, each_path_lenth


