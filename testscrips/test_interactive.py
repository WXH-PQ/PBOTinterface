# !/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
sys.path.append('../')
from testscrips import *
from resources import  *


logger = Logger(logger="Interactive").getlog()
current_dir = os.getcwd()
filename = os.path.join(os.path.dirname(current_dir), 'testcases',read_config("CASE_NAME","interactive"))
cases = get_params(filename,'Sheet1')
start_time = date_format('now-1')
end_time = ""


@allure.feature("通话交互模块")
class Testinteractive:
    @pytest.fixture(scope='class',autouse=True)
    def setup_class(self,delay,t_start,UUID):
        '''此方法只执行一次，跑测试脚本之前先拿到测试数据'''
        logger.info("通话交互模块测试开始！！")

        yield
        logger.info("通话交互模块测试结束！！")


    @allure.title("通话交互crs响应数据正常")
    @pytest.mark.parametrize('case',cases)
    def test_001(self,UUID,case):
        # 处理call_id
        case["call_id"] = case["call_id"] + '-' +  UUID
        # 处理时间参数，如用例上传了则用用例的，如果没有传则自己生成
        time_key = ['start_time','begin_play','end_play','flow_result_time']
        for  key in time_key:
            if case[key] == "":
                case[key] = date_format('now')

        logger.info("测试参数为：")
        logger.info(str(case))
        response = interactive(case)
        logger.info("crs响应为：")
        logger.info(str(response))

        for key in case.keys():
            if "R_" in key :
                k = key.split("R_")[1]
                if case[key] != "" and case[key] != '空':
                    if k == "outaction" or k == "ret":
                        assert case[key] == str(response[k])
                    elif k == "call_id":
                        assert case[key] + '-' + UUID == str(response["outparams"][k])
                    else:
                        assert case[key] == str(response["outparams"][k])

                if  case[key] == '空':
                    assert  str(response['outparams'][k]) == ''



    @allure.title("通话交互入库数量正常")
    @pytest.mark.flaky(reruns=4, reruns_delay=10)
    @pytest.mark.parametrize('count', [13])
    def test_002(self,t_start,count):
        logger.info("通话交互入库数量测试开始")
        end_time = date_format('now-1')
        data_dic = {
            'conditions' : {"call_time_start" : t_start ,"call_time_end": end_time },
            'call_label':'',
            'date_start':date_format('mouth'),
            'date_end':date_format('mouth'),
            'flip':''
        }
        logger.info("查询条件为：")
        logger.info(str(data_dic))
        count_actual = data_filter_count(data_dic)
        assert count_actual == count
