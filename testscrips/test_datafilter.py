# !/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import allure
import pytest
sys.path.append('../')
from resources import  *
from testscrips import *

logger = Logger(logger="Datafilter").getlog()
current_dir = os.getcwd()
filename = os.path.join(os.path.dirname(current_dir), 'testcases',read_config("CASE_NAME","datafilter"))
cases = get_params(filename,'数据筛选用例')
cases_call_info = get_params(filename,'通话明细')


@allure.feature("数据筛选模块")
class Testdatafilter:
    @pytest.fixture(scope='class',autouse=True)
    def setup_class(self,UUID):
        logger.info("数据筛选模块测试开始！！！")
        logger.info("产生测试数据")
        create_data(filename,'交互用例',UUID)
        logger.info("产生测试数据完成")

        yield
        logger.info("数据筛选模块测试完成")

    @allure.title("数据筛选结果数据正确")
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.parametrize('case',cases)
    def test_001(self,UUID,case):
        data_dic = deal_datafilter(case,UUID)
        logger.info("数据筛选输入条件为：")
        logger.info(str(data_dic))

        response = data_filter(data_dic)

        logger.info("数据筛选结果为：")
        logger.info(str(response))

        # 提取查询结果的call_id
        call_id_actual = []
        call_id_expect = []
        for row in response['rows']:
            call_id_actual.append(row['call_id'])

        # 处理期望call_id
        call_ids = list(case['R_call_id'].split(","))
        if case['new|old'] == 'new':
            for i in  range(0,len(call_ids)):
                call_id_expect.append(call_ids[i] + '-' + UUID)
        else:
            call_id_expect = call_ids

        assert  call_id_actual == call_id_expect


    @allure.title("通话明细数据正确")
    @pytest.mark.parametrize('case',cases_call_info)
    def test_002(self,UUID,case):
        case['call_id'] = case['call_id'] + '-' + UUID
        logger.info("通话明细期望结果为：")
        logger.info(case)

        resources = call_info(case)
        actual_call_info = deal_call_info(resources)

        logger.info("通话明细实际结果为：")
        logger.info(actual_call_info)
        assert actual_call_info == case['通话明细']


