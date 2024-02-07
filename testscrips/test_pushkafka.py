# !/usr/bin/env python
# -*- coding=utf-8
import sys
sys.path.append('../')
import sys
from testscrips import  *
from utils import *
from resources import  *


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = Logger(logger="pushkafka").getlog()
current_dir = os.getcwd()
filename = os.path.join(os.path.dirname(current_dir), 'testcases', read_config("CASE_NAME", "pushkafka"))
case_call = get_params(filename,"通话计费数据")
case_inter = get_params(filename,"交互计费数据")


@allure.feature("计费模块")
class Testpushkafka:
    @pytest.fixture(scope='class',autouse=True)
    def setup_class(self,UUID):
        logger.info("计费推送模块测试开始！！")
        logger.info("产生测试数据")
        create_data(filename,'交互用例',UUID)
        logger.info("产生测试数据完成")

        yield
        logger.info("计费推送模块测试结束！！")

    @allure.title("计费数据-通话数据正确")
    @pytest.mark.flaky(reruns=3,reruns_delay=10)
    @pytest.mark.parametrize('case',case_call)
    def test_001(self,UUID,case):
        if case["call_id"] == '' or case["call_id"] == 'no':
            pass
        else:
            logger.info("期望计费数据-通话数据为：")
            logger.info(str(case))
            # 获取数据库计费数据通话表中对应call_id数据内容
            sql = "SELECT * from aicall_call_D WHERE call_id = '" + case['call_id'] + "-" + UUID + "'"
            m = mysql(read_config('KAFKA','DB_HOST'),read_config('KAFKA','DB_PORT'),read_config('KAFKA','DB_USER'),read_config('KAFKA','DB_PASSWORD'),read_config('KAFKA','DB_DATABASE'))
            result = m.sqlOperate(sql)[0]
            logger.info("实际计费数据-通话数据为：")
            logger.info(str(result))
            # 删除数据库结果的"id"
            del result['id']
            # 断言期望结果和实际结果的字段个数是否一致
            assert len(case) == len(result)
            # 断言期望结果和实际结果的字段内容是否一致
            for key in case.keys():
                if case[key] != "":
                    if key == 'statis_date' or key == 'start_time' or key == 'end_time':
                        assert result[key] != ""
                    elif case[key] == '空':
                        assert result[key] == ""
                    elif key == 'call_id':
                        assert  case[key] + '-' + UUID == result[key]
                    else:
                        assert case[key] == result[key]


    @allure.title("计费数据-轮次数据正确")
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.parametrize('case',case_inter)
    def test_002(self,UUID,case):
        if case["call_id"] == '' or case["call_id"] == 'no':
            pass
        else:
         #   case['call_id'] = case['call_id'] + '-' + UUID
            logger.info("期望计费数据-轮次数据为：")
            logger.info(str(case))
            # 获取数据库计费数据轮次表中对应call_id的数据内容
            sql = "SELECT * from aicall_inter_D WHERE call_id = '" + case['call_id'] + "-" + UUID + "' and inter_idx = '" + case['inter_idx'] + "'"
            m = mysql(read_config('KAFKA', 'DB_HOST'), read_config('KAFKA', 'DB_PORT'), read_config('KAFKA', 'DB_USER'),
                      read_config('KAFKA', 'DB_PASSWORD'), read_config('KAFKA', 'DB_DATABASE'))
            result = m.sqlOperate(sql)[0]
            logger.info("实际计费数据-轮次数据为：")
            logger.info(str(result))

            # 删除数据库结果的"id"
            del result['id']
            # 断言期望结果和实际结果的字段个数是否一致
            assert len(case) == len(result)
            # 断言期望结果和实际结果的字段内容是否一致
            for key in case.keys():
                if case[key] != '':
                    if key == 'statis_date' or key == 'begin_time' or key == 'finish_time' or key == 'commun_id' or key == 'crs_res_time':
                        assert result[key] != ""
                    elif key == 'call_id':
                        assert  case[key] + '-' + UUID == result[key]
                    else:
                        assert case[key] == result[key]

