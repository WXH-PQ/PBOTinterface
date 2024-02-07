import sys
sys.path.append('../')
import sys
from utils import *
from resources import  *

# 产生通话数据方法，传入用例文件名、sheet名称
def create_data(filename,sheet_name,UUID):
    case = get_params(filename,sheet_name)
    for i in case:
        if  i["call_id"] == 'no':
            pass
        else:
            i['call_id'] = i['call_id'] + '-' + UUID
            interactive(i)

# 处理数据筛选测试用例方法，传入case(单条)，uuid
def deal_datafilter(case,UUID):
    data_dic = {}
    conditions = {}
    for key in case.keys():
        if key == 'call_label' or key == 'flip':
            data_dic[key] = case[key]
        elif key == 'date_start' or key == 'date_end':
            if case[key] == "":
                data_dic[key] = date_format('mouth')
            else:
                data_dic[key] = case[key]
        elif key == 'call_id' and case[key] != '':
            if case['new|old'] == 'new':
                conditions[key] = case[key] + '_' + UUID
            else:
                conditions[key] = case[key]
        elif key == 'call_time_start':
            if case[key] == '':
                start = date_format('day') + ' 00:00:00'
                conditions['call_time_start'] = start
            else:
                conditions['call_time_start'] = case[key]
        elif key == 'call_time_end':
            if case[key] == '':
                end = date_format('day') + ' 23:59:59'
                conditions['call_time_end'] = end
            else:
                conditions['call_time_start'] = case[key]
        elif case[key] != '' and 'R_' not in key and key != 'new|old':
            conditions[key] = case[key]
    data_dic['conditions'] = conditions
    return data_dic

# 处理通话明细接口返回的数据，传入接口原本返回值（单条）,返回整通对话的文本列表
def deal_call_info(res):
    call_info = []
    if res['data'] != None:
        for i in res['data']:
            if i['content'] == '':
                call_info.append('空')
            else:
                call_info.append(i['content'])

    return "|".join(call_info)