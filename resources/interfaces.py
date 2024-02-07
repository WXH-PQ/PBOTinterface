# !/usr/bin/env python
# -*- coding=utf-8 -*-
import json

from utils import *

# 通话交互接口，传入的data是一组词典
def interactive(data_dic):
    url = "http://" + read_config("HOST","IP")  + ":" + read_config("HOST","PORT") + "/pbot/gray-sc/crs"
    header = {"Content-Type":"application/json"}


    # 第一轮
    if data_dic["inaction"] == "8":
        data = {
            "userid" : data_dic["call_id"],
            "task_id": data_dic["call_id"],
            "inaction" : data_dic["inaction"],
            "prov_id" : data_dic["prov_id"],
            "sample_id" : data_dic["sample_id"],
            "channel_type" : "",
            "inparams" : {
                "call_id" : data_dic["call_id"],
                "call_sor_id" : "10086",
                "call_dst_id" : data_dic["call_dst_id"],
                "entrance_id": data_dic["entrance_id"],
                "start_time": data_dic["start_time"],
                "flow": "root.xml",
                "ses_time" : "",
                "suilu_region_id" : "0313",
                "region_id" : data_dic["region_id"],
                "cc_id" : "",
                "role_label" : "",
                "panoramic_wav" : "1.wav",
                "auth_token" : ""
            }
        }
    # 中间轮
    if  data_dic["inaction"] == "9" :
        data = {
            "userid": data_dic["call_id"],
            "task_id": data_dic["call_id"],
            "inaction": data_dic["inaction"],
            "prov_id": data_dic["prov_id"],
            "sample_id" : data_dic["sample_id"],
            "channel_type": "",
            "inparams": {
                "call_id": data_dic["call_id"],
                "inter_idx" : data_dic["inter_idx"],
                "flow_result_type": data_dic["flow_result_type"],
                "input": data_dic["input"],
                "begin_play" : data_dic["begin_play"],
                "end_play" : data_dic["end_play"],
                "result_time" : data_dic["result_time"],
                "flow_result_time": data_dic["flow_result_time"],
                "inter_no" : data_dic["inter_no"],
                "res_node_lst" : "",
                "res_parse_mode" : "",
                "extended_field": ""
            }
        }

    # 挂接节点
    if data_dic["input"] == "hangup":
        data = {
            "userid": data_dic["call_id"],
            "task_id": data_dic["call_id"],
            "inaction": data_dic["inaction"],
            "prov_id": data_dic["prov_id"],
            "sample_id": data_dic["sample_id"],
            "channel_type": "",
            "inparams": {
                "call_id": data_dic["call_id"],
                "inter_idx": data_dic["inter_idx"],
                "flow_result_type": data_dic["flow_result_type"],
                "input": data_dic["input"],
                "begin_play" : data_dic["begin_play"],
                "end_play" : data_dic["end_play"],
                "result_time" : data_dic["result_time"],
                "flow_result_time": data_dic["flow_result_time"],
                "inter_no" : data_dic["inter_no"],
                "org" : "",
                "res_node_lst": "",
                "newsess" : "",
                "only_fill_slot" : "",
                "res_parse_mode": "",
                "crs_err_code": ""
            }
        }


    # data_json = json.dumps(data,ensure_ascii=False)
    # print("tpye:",type(data_json))
    response = fun_post(url,header,data)
    return  response

# 精简报表接口，只需要传入url 和 token
def reportforms(day,mouth):
    url = 'http://' + read_config("HOST","IP") + ":" + read_config("HOST","PORT_WEB") + '/pbot/audio/iod/report/part/download/?'\
      'conditions={"call_time_start":"' + day + ' 00:00:00","call_time_end":"' + day + ' 23:59:59","entrance_id":"001"}&call_label=&date_start=' + mouth + '&date_end=' + mouth + '&type=""'

    header = {"Content-Type":"application/json","Token":"PBOT_PHX_4_2:" + read_config("TOKEN","TOKEN")}

    response = requests.post(url, headers=header, data='').text

    return response


# 话务管理系统数据筛选接口，传入的data_dic 是一组词典
def data_filter(data_dic):
    header = {"Content-Type":"application/json","Token":"PBOT_PHX_4_2:" + read_config("TOKEN","TOKEN")}
    url = 'http://' + read_config("HOST","IP") + ":" + read_config("HOST","PORT_WEB") + '/pbot/audio/iod/report/call_list/?' \
    'conditions=' + json.dumps(data_dic['conditions']) + '&page_size=20&call_label=' + data_dic['call_label'] + '&date_start=' + str(
    data_dic['date_start']) + '&date_end=' + str(data_dic['date_end']) + '&flip=' + data_dic['flip'] + '&min_id=0&max_id=0&chiasm=home'

    response = fun_get(url,header,params="")
    return response

# 话务管理系统数据筛选接口（只返回数据数量），传入的data_dic 是一组词典,返回数量（整数）
def data_filter_count(data_dic):
    header = {"Content-Type": "application/json", "Token": "PBOT_PHX_4_2:" + read_config("TOKEN", "TOKEN")}

    url = 'http://' + read_config("HOST","IP") + ':' + read_config("HOST","PORT_WEB") + '/pbot/audio/iod/report/call_count/?'\
    'conditions=' + json.dumps(data_dic['conditions']) + '&page_size=20&call_label=' + data_dic['call_label'] + '&date_start=' + str(data_dic['date_start']) + \
    '&date_end=' + str(data_dic['date_end']) + '&flip=' + data_dic['flip'] + '&min_id=0&max_id=0&chiasm=home'

    response = fun_get(url,header,params="")
    count = int(response['count'])
    return  count

# 话务系统查看通话明细的接口
def call_info(data_dic):
    header = {"Content-Type":"application/json","Token":"PBOT_PHX_4_2:" + read_config("TOKEN","TOKEN")}

    url = 'http://' + read_config("HOST","IP") + ":" + read_config("HOST","PORT_WEB") + '/pbot/audio/iod/report/call_info?' \
    'call_id=' + data_dic['call_id'] + '&date=' + date_format('mouth')

    response = fun_get(url,header,params="")
    return response